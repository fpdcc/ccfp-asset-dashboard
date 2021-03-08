import pytest
from asset_dashboard import models

@pytest.fixture
def section_owner():
    """
    Creates and returns a section owner.
    """
    return models.Section.objects.create(name="Architecture")


@pytest.fixture
def project_category():
    return models.ProjectCategory.objects.create(category='land improvement', subcategory='restoration')


@pytest.fixture
def project(section_owner, project_category):
    """
    Creates and returns a single project.
    """

    project = models.Project.objects.create(name="Trail Maintenance", 
                                            description="Fixing trail erosion.", 
                                            section_owner=section_owner,
                                            category=project_category)
    
    project_score = models.ProjectScore.objects.create(project=project)

    return project


@pytest.fixture
def project_list():
    """
    Creates and returns a QuerySet of all projects.
    """

    for index in range(10):
        name = f'project_{index}'
        description = f'description text for this project'
        section_owner = models.Section.objects.create(name=f'Section{index}')
        category = models.ProjectCategory.objects.create(category=f'category {index}', subcategory=f'subcategory {index}')
        project = models.Project.objects.create(name=name, description=description, section_owner=section_owner, category=category)
        project_score = models.ProjectScore.objects.create(project=project)

    return models.Project.objects.all()


@pytest.fixture
def districts():
    """
    Creates the different geographic districts.
    """
    
    for index in range(6):
        fake_district_name = f'District {index+1}'
        models.SenateDistrict.objects.create(name=fake_district_name)
        models.HouseDistrict.objects.create(name=fake_district_name)
        models.CommissionerDistrict.objects.create(name=fake_district_name)
        models.Zone.objects.create(name=f'Zone {index+1}')

    senate_districts = models.SenateDistrict.objects.all()
    house_districts = models.HouseDistrict.objects.all()
    commissioner_districts = models.CommissionerDistrict.objects.all()
    zones = models.Zone.objects.all()
    
    return senate_districts, house_districts, commissioner_districts, zones


@pytest.fixture
def score_weights():
    return models.ScoreWeights.objects.create(core_mission_score=0.7, operations_impact_score=0.8, 
                                              sustainability_score=0.2, ease_score=0.6, 
                                              geographic_distance_score=0.5, social_equity_score=0.4,
                                              obligation_weight=0.5, phase_completion=0.5, 
                                              accessibility=0.5, leverage_resource=0.5)

@pytest.fixture
def user():
    return models.User.objects.create_user(username='sylvie', password='lightnin')
