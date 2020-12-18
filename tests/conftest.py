import pytest
from asset_dashboard import models

@pytest.fixture
def project():
    """
    Creates and returns a single project.
    """

    return models.Project.objects.create(name="Trail Maintenance", description="Fixing trail erosion.")


@pytest.fixture
def project_list():
    """
    Creates and returns a QuerySet of all projects.
    """

    for index in range(10):
        name = f'project_{index}'
        description = f'description text for this project'
        models.Project.objects.create(name=name, description=description)

    return models.Project.objects.all()
