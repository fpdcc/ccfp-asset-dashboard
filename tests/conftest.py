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

    section_owner = models.Section.objects.create(name="Civil Engineering")

    for index in range(10):
        name = f'project_{index}'
        description = f'description text for this project'
        project = models.Project.objects.create(name=name, description=description, section_owner=section_owner)
        project_score = models.ProjectScore.objects.create(project=project)
        category = models.ProjectCategory.objects.create(project=project, category=f'improvement {index}', subcategory=f'sub {index}')

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
