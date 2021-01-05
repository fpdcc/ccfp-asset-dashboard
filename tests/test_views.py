import pytest
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
def test_add_project_view(client, section_owner):
    url = reverse('add-project')

    valid_form_data = {
        'name': 'trail maintenance project',
        'description': 'We need to clean the trail and fix some washouts.',
        'section_owner': section_owner.pk
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
def test_project_update_view(client, project, project_list, section_owner):
    url = reverse('project-detail', kwargs={'pk': project.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['project'] == project

    # test bad url does not exist
    bad_url = reverse('project-detail', kwargs={'pk': 1234556873459})
    bad_response = client.get(bad_url)
    assert bad_response.status_code == 404

    # test that the project UpdateView can update the model instance
    valid_form_data = {
        'name': 'trail improvement project',
        'description': 'We need to clean the trail, fix some washouts, and build a bathroom.',
        'section_owner': section_owner.pk
    }
    successful_response = client.post(url, data=valid_form_data)
    assert successful_response.status_code == 302

    # test that the form saved the project with correct data
    updated_project = Project.objects.filter(name=valid_form_data['name'])
    assert updated_project[0].name == valid_form_data['name']
    assert updated_project[0].description == valid_form_data['description']

    # test that only one project was updated
    assert updated_project.count() == 1

    # test that the project updated and renders the updated data to the project ListView
    response = client.get(reverse('projects'))
    assert valid_form_data['name'] in str(response.context)

    # test that the project UpdateView did not overwrite any of the other projects
    existing_project_name = 'project_0'
    assert existing_project_name in str(response.context)
