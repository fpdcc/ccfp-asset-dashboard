import json
import pytest
from django.db import IntegrityError

from asset_dashboard.models import ScoreWeights, Portfolio, PortfolioPhase, \
    LocalAsset, SenateDistrict, Phase, PhaseZoneDistribution, FundingStream, Project, \
    ProjectScore


@pytest.mark.django_db
def test_project_score_total_method(project, score_weights):
    """
    Tests the ProjectScore.total_score method
    """
    project = project.build()
    project_score_instance = project.projectscore

    # When a project is created, all of the ProjectScore fields equal 0.
    # So, test that total_score = 0.
    assert project_score_instance.total_score == 0

    updated_scores = {
        'core_mission_score': 3,
        'operations_impact_score': 1,
        'ease_score': 5,
        'sustainability_score': 7,
        'geographic_distance_score': 6,
        'social_equity_score': 5
    }

    project_score_instance.__dict__.update(updated_scores)
    project_score_instance.save()

    # calculate the score "by hand" (within this test)
    total_score = 0
    weights_sum = 0
    for index, score_field_name in enumerate(updated_scores):
        weight_field_value = getattr(score_weights, score_field_name)
        weights_sum += weight_field_value

        score_field_value = getattr(project_score_instance, score_field_name)
        total_score += score_field_value * weight_field_value

    assert pytest.approx(project_score_instance.total_score) == total_score / weights_sum

    # test that an error will raise if there is no score weight
    with pytest.raises(ValueError):
        ScoreWeights.objects.all().delete()

        # this should raise an error
        project_score_instance.total_score

    # test that an error will raise if there is more than one score weight
    with pytest.raises(ValueError):
        ScoreWeights.objects.create(core_mission_score=0.7, operations_impact_score=0.8,
                                              sustainability_score=0.2, ease_score=0.6,
                                              geographic_distance_score=0.5, social_equity_score=0.4)

        ScoreWeights.objects.create(core_mission_score=0.7, operations_impact_score=0.8,
                                              sustainability_score=0.2, ease_score=0.6,
                                              geographic_distance_score=0.5, social_equity_score=0.4)

        # this should raise an error
        project_score_instance.total_score


@pytest.mark.django_db
def test_sequenced_model(user, project):
    project_a = project.build()
    project_b = project.build(name='Some other project')
    project_c = project.build(name='Still some other project')

    portfolio = Portfolio.objects.create(user=user)

    phase_a = PortfolioPhase.objects.create(
        portfolio=portfolio,
        phase=project_a.phases.get()
    )

    assert phase_a.sequence == 1

    phase_b = PortfolioPhase.objects.create(
        portfolio=portfolio,
        phase=project_b.phases.get(),
        sequence=1
    )

    phase_a.refresh_from_db()

    assert phase_b.sequence == 1
    assert phase_a.sequence == 2

    phase_c = PortfolioPhase.objects.create(
        portfolio=portfolio,
        phase=project_c.phases.get(),
        sequence=2
    )

    for phase in (phase_a, phase_b):
        phase.refresh_from_db()

    assert phase_b.sequence == 1
    assert phase_c.sequence == 2
    assert phase_a.sequence == 3

# @pytest.mark.django_db(databases=['default', 'fp_postgis'])
# def test_local_asset_signal(project, phase_assets, phase_funding, districts, trails_geojson, socio_economic_zones, score_weights, zones):
#     project_a = project.build()
#     phase = Phase.objects.filter(project=project_a)[0]
#     phase_assets.build(phase=phase)
#     phase_funding.build(phase=phase)

#     phase.refresh_from_db()
#     project_a.refresh_from_db()

#     assert project_a.projectscore.total_score > 0
#     assert project_a.senate_districts.all().count() > 0
#     assert project_a.house_districts.all().count() > 0
#     assert project_a.commissioner_districts.all().count() > 0
#     assert project_a.zones.count() > 0

@pytest.mark.django_db(databases=['default', 'fp_postgis'])
def test_phase_zone_distribution_post_save_signal(
    project, zones, signs_geojson, trails_geojson, socio_economic_zones, districts, score_weights
):
    prj = project.build()
    phase = Phase.objects.filter(project=prj)[0]

    for feature in signs_geojson['features']:
        asset = LocalAsset.objects.create(
            phase=phase, geom=json.dumps(feature['geometry'])
        )

    phase.refresh_from_db()

    phase_zone_distributions = PhaseZoneDistribution.objects.filter(phase=phase)
    assert (
        sum([dist.zone_distribution_proportion for dist in phase_zone_distributions])
        == 1.0
    )

    zone_with_all_geos = list(
        filter(lambda d: d.zone_distribution_proportion > 0, phase_zone_distributions)
    )
    assert len(zone_with_all_geos) == 1

    # Add some more assets, which should change the distribution.
    for feature in trails_geojson['features']:
        asset = LocalAsset.objects.create(
            phase=phase, geom=json.dumps(feature['geometry'])
        )

    # Query the new distributions. They should've changed when the new assets were created.
    phase_zone_distributions_reload = PhaseZoneDistribution.objects.filter(phase=phase)
    zones_with_geos = list(
        filter(
            lambda d: d.zone_distribution_proportion > 0,
            phase_zone_distributions_reload,
        )
    )
    assert len(zones_with_geos) > 1
    assert (
        sum(
            [
                round(dist.zone_distribution_proportion)
                for dist in phase_zone_distributions_reload
            ]
        )
        == 1.0
    )

    # Add an estimated cost to the phase so we can test the total cost by zone.
    funding_stream = FundingStream.objects.create(
        budget=250000,
        year=2023,
        funding_secured=True,
    )
    phase.funding_streams.add(funding_stream)
    phase.save()

    for distribution in phase_zone_distributions_reload:
        cost = phase.cost_by_zone.get(distribution.zone.name)
        assert cost == 250000 * distribution.zone_distribution_proportion

    # Test delete signal
    assets = LocalAsset.objects.filter(phase=phase)
    for asset in assets:
        asset.delete()

    phase.refresh_from_db()
    phase_zone_distributions = PhaseZoneDistribution.objects.filter(phase=phase)
    assets = LocalAsset.objects.filter(phase=phase)
    for zone_dist in phase_zone_distributions:
        assert zone_dist.zone_distribution_proportion == 0.0


@pytest.mark.django_db(databases=['default', 'fp_postgis'])
def test_phase_zone_distribution_delete_phase(
    project, assets, phase_funding, zones, socio_economic_zones, districts, score_weights
):
    prj = project.build()
    phase = Phase.objects.filter(project=prj)[0]
    assets.build(phase=phase)
    phase_funding.build(phase=phase)

    # Get a record of these, because we'll test their existence after the phase is deleted
    distributions = PhaseZoneDistribution.objects.filter(phase=phase)

    for phase in prj.phases.all():
        phase.delete()

    prj.refresh_from_db()
    phases = prj.phases.all()
    assert len(phases) == 0

    for distribution in distributions:
        # try to get the distribution with the key. it should not exist
        with pytest.raises(IntegrityError):
            PhaseZoneDistribution.objects.get(pk=distribution.pk)


@pytest.mark.django_db(databases=['default', 'fp_postgis'])
def test_assets_calculation_robustly(project, phase_assets, zones, socio_economic_zones, districts, score_weights):
    """
    Regression test for a bug that would sometimes crash postgres when calculating all of the GIS totals for a phase.
    Occurred when the GIS assets were located far away from each other. This test uses phase_assets
    that are located across the entire county, in order to make sure the database doesn't crash.
    """
    prj = project.build()
    phase = Phase.objects.filter(project=prj)[0]
    phase_assets.build(phase=phase)

    phase_zone_distributions = PhaseZoneDistribution.objects.filter(phase=phase)
    assert phase_zone_distributions

    prj.refresh_from_db()
    assert prj.projectscore.total_score > 0
    assert prj.senate_districts.all().count() > 0
    assert prj.house_districts.all().count() > 0
    assert prj.commissioner_districts.all().count() > 0
    assert prj.zones.count() > 0


@pytest.mark.django_db(databases=['default', 'fp_postgis'])
def test_project_delete(project, phase_assets, zones, socio_economic_zones, districts, score_weights):
    prj = project.build()
    phase = Phase.objects.filter(project=prj)[0]
    phase_assets.build(phase=phase)

    # get these ids before deleting the project,
    # so later we can test they don't exist anymore
    project_id = prj.id
    project_score_id = prj.projectscore.id
    phase_id = phase.id
    phase_asset_ids = [asset.id for asset in LocalAsset.objects.filter(phase=phase)]

    # should work without a problem
    prj.delete()

    # test these things don't exist anymore
    with pytest.raises(Project.DoesNotExist):
        Project.objects.get(id=project_id)

    with pytest.raises(ProjectScore.DoesNotExist):
        ProjectScore.objects.get(id=project_score_id)

    with pytest.raises(Phase.DoesNotExist):
        Phase.objects.get(id=phase_id)

    for asset_id in phase_asset_ids:
        with pytest.raises(LocalAsset.DoesNotExist):
            LocalAsset.objects.get(id=asset_id)


