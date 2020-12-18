import pytest
from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse
from asset_dashboard.models import Project

@pytest.mark.django_db
def test_project_list_view(client, project_list):
    url = reverse('projects')
    response = client.get(url)
    assert response.status_code == 200
    assert list(project_list) == list(response.context['projects'])
    assert project_list[0] == response.context['projects'][0]


@pytest.mark.django_db
def test_add_project_view(client):
    url = reverse('add-edit-projects')

    valid_form_data = {
        'name': 'trail maintenance project',
        'description': 'We need to clean the trail and fix some washouts.'
    }

    successful_response = client.post(url, data=valid_form_data)

    # assert that the new project saved successfully
    new_project_from_form = Project.objects.filter(name=valid_form_data['name'])[0]
    assert new_project_from_form.name == valid_form_data['name']
    assert new_project_from_form.description == valid_form_data['description']

    # user should be redirected to the new project detail page
    assert successful_response.status_code == 302

    # the new project's detail page should be at this route: /projects/<pk:int>
    # so make sure the new project PK is in the response's redirect url
    assert str(new_project_from_form.pk) in successful_response.url

    invalid_form_data = [
        {'name': '', 'description': ''},
        {'name': ''},
        {'description': ''},
        {'name': 'name without description'},
        {'description': 'description without name'}
    ]

    for form_data in invalid_form_data:
        invalid_response = client.post(url, data=form_data)
        assert invalid_response.status_code == 400


@pytest.mark.django_db
def test_project_detail_view(client, project):
    url = reverse('project-detail', kwargs={'pk': project.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['project'] == project

    # test bad url
    bad_url = reverse('project-detail', kwargs={'pk': 1234556873459})
    bad_response = client.get(bad_url)
    assert bad_response.status_code == 404