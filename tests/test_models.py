import pytest
from asset_dashboard.models import ScoreWeights, Portfolio, PortfolioPhase


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
