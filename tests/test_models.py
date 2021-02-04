import pytest
from asset_dashboard.models import ProjectScore

@pytest.mark.django_db
def test_project_score_total_method(project, score_weights):
    """
    Tests the ProjectScore.total_score method
    """
    print('test project score')
    print(score_weights)
    
    project_score_instance = project.projectscore
    
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
