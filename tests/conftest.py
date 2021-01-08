import pytest
from asset_dashboard import models

@pytest.fixture
def project():
    """
    Creates and returns a single project.
    """
    section_owner = models.Section.objects.create(name="Architecture")

    project = models.Project.objects.create(name="Trail Maintenance", 
                                        description="Fixing trail erosion.", 
                                        section_owner=section_owner)
    
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
        print('project score')
        print(project_score)

    return models.Project.objects.all()


@pytest.fixture
def section_owner():
    """
    Creates and returns a section owner.
    """
    return models.Section.objects.create(name="Architecture")
