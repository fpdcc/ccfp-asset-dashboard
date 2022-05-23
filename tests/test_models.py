import json
import pytest
from asset_dashboard.models import ScoreWeights, Portfolio, PortfolioPhase, \
    LocalAsset, SenateDistrict, Phase, PhaseZoneDistribution


@pytest.mark.django_db
def test_project_score_total_method(project, score_weights):
    """
    Tests the ProjectScore.total_score method
    """
    project = project.build()
    project_score_instance = project.projectscore

    # at this point in the code, the ProjectScore fields have no data.
    # so, test that total_score = 0 if there is a missing score
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
    for index, score_field_name in enumerate(updated_scores):
        weight_field_value = getattr(score_weights, score_field_name)
        score_field_value = getattr(project_score_instance, score_field_name)
        total_score += score_field_value * weight_field_value

    assert project_score_instance.total_score == total_score

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

@pytest.mark.django_db
def test_local_asset_signal(project, districts, trails_geojson):
    senate_districts = SenateDistrict.objects.all()
    project_a = project.build()

    phase = Phase.objects.filter(project=project_a)[0]

    for feature in trails_geojson['features']:
        asset = LocalAsset.objects.create(
            phase=phase,
            geom=json.dumps(feature['geometry'])
        )

        assert asset.phase.project.senate_districts.all()[0] in senate_districts
    
@pytest.mark.django_db
def test_phase_zone_distribution_signal(project, zones, signs_geojson, trails_geojson):
    prj = project.build()
    phase = Phase.objects.filter(project=prj)[0]
    
    for feature in signs_geojson['features']:
        asset = LocalAsset.objects.create(
            phase=phase,
            geom=json.dumps(feature['geometry'])
        )
    
    phase_zone_distributions = PhaseZoneDistribution.objects.filter(phase=phase)
    assert sum([dist.zone_distribution_proportion for dist in phase_zone_distributions]) == 1.0

    zone_with_all_geos = list(filter(lambda d: d.zone_distribution_proportion > 0, phase_zone_distributions))
    assert len(zone_with_all_geos) == 1
    
    # Add some more assets, which should change the distribution.
    for feature in trails_geojson['features']:
        asset = LocalAsset.objects.create(
            phase=phase,
            geom=json.dumps(feature['geometry'])
        )

    # Query the new distributions. They should've changed when the new assets were created.
    phase_zone_distributions_reload = PhaseZoneDistribution.objects.filter(phase=phase)
    zones_with_geos = list(filter(lambda d: d.zone_distribution_proportion > 0, phase_zone_distributions_reload))
    assert len(zones_with_geos) > 1
    assert sum([round(dist.zone_distribution_proportion) for dist in phase_zone_distributions_reload]) == 1.0

    # Add an estimated cost to the phase so we can test the total cost by zone.
    # TODO: calculate this with new attribute
    # phase.total_estimated_cost = 250000
    # phase.save()

    for distribution in phase_zone_distributions_reload:
        cost = phase.cost_by_zone.get(distribution.zone.name)
        assert cost == 250000 * distribution.zone_distribution_proportion


    # Test delete signal
    assets = LocalAsset.objects.filter(phase=phase)
    for asset in assets:
        asset.delete()
    
    phase_zone_distributions = PhaseZoneDistribution.objects.filter(phase=phase)
    for zone_dist in phase_zone_distributions:
        assert zone_dist.zone_distribution_proportion == 0.0

        