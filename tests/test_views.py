import pytest
from django.urls import reverse
from asset_dashboard.models import Project, ProjectScore
from django.forms.models import model_to_dict

from pprint import pprint

@pytest.mark.django_db
def test_project_list_view(client, project_list):
    url = reverse('projects')
    response = client.get(url)
    assert response.status_code == 200
    assert list(project_list) == list(response.context['projects'])
    assert project_list[0] == response.context['projects'][0]


@pytest.mark.django_db
def test_add_project_view(client, section_owner, project_category):
    url = reverse('add-project')

    valid_form_data = {
        'name': 'trail maintenance project',
        'description': 'We need to clean the trail and fix some washouts.',
        'section_owner': section_owner.pk,
        'category': project_category.pk
    }

    successful_response = client.post(url, data=valid_form_data)

    # assert that the new project saved successfully
    new_project_from_form = Project.objects.filter(name=valid_form_data['name'])[0]
    assert new_project_from_form.name == valid_form_data['name']
    assert new_project_from_form.description == valid_form_data['description']
    
    # a ProjectScore should've been created, too
    project_score = ProjectScore.objects.filter(project=new_project_from_form)
    assert project_score.exists()
    assert project_score.count() == 1

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
        assert invalid_response.context['form'].errors
    

@pytest.mark.django_db
def test_project_detail_view(client, project, project_list, section_owner, districts, project_category):
    project_detail_url = reverse('project-detail', kwargs={'pk': project.pk})
    response = client.get(project_detail_url)
    assert response.status_code == 200

    project_from_response = response.context['project']
    project_score_from_response = response.context['project'].projectscore

    assert project_from_response == project
    assert project_score_from_response == project.projectscore

    # prepare the data to be submitted via form
    valid_form_data = {}
    valid_form_data.update(model_to_dict(project_from_response))
    valid_form_data.update(model_to_dict(project_score_from_response))
    
    # change some of the fields
    valid_form_data.update({
        'name': 'trail maintenance',
        'description': 'fixing erosion',
        'category': project_category.id,
        'section_owner': section_owner.id,
        'core_mission_score': 2,
        'operations_impact_score': 3,
        'sustainability_score': 4,
        'ease_score': 4,
        'geographic_distance_score': 1,
        'social_equity_score': 3,
        'phase_completion': 'on',
        'senate_districts': [districts[0][0].id],
        'house_districts': [districts[1][0].id],
        'commissioner_districts': [districts[2][0].id],
        'zones': [districts[3][0].id]
    })

    # test the form submission
    successful_response = client.post(project_detail_url, data=valid_form_data)
    assert successful_response.status_code == 302

    # test that the form submission saved the project with correct data for all the fields
    updated_project = Project.objects.filter(name=valid_form_data['name'])
    
    # Project model
    assert updated_project[0].name == valid_form_data['name']
    assert updated_project[0].description == valid_form_data['description']
    assert updated_project[0].phase_completion == True
    assert updated_project[0].category_id == project_category.id
    assert updated_project[0].section_owner_id == section_owner.id
    
    # ProjectScore model, related to Project
    assert updated_project[0].projectscore.core_mission_score == valid_form_data['core_mission_score']
    assert updated_project[0].projectscore.operations_impact_score == valid_form_data['operations_impact_score']
    assert updated_project[0].projectscore.sustainability_score == valid_form_data['sustainability_score']
    assert updated_project[0].projectscore.ease_score == valid_form_data['ease_score']
    assert updated_project[0].projectscore.geographic_distance_score == valid_form_data['geographic_distance_score']
    assert updated_project[0].projectscore.social_equity_score == valid_form_data['social_equity_score']
    
    # Districts, related to Project
    assert updated_project[0].senate_districts.all()[0] == districts[0][0]
    assert updated_project[0].house_districts.all()[0] == districts[1][0]
    assert updated_project[0].commissioner_districts.all()[0] == districts[2][0]
    assert updated_project[0].zones.all()[0] == districts[3][0]

    # test that only one project was updated
    assert updated_project.count() == 1

    # test that the project updated and renders the updated data to the project ListView
    # this is to ensure a bug doesn't creep back in
    response = client.get(reverse('projects'))
    assert valid_form_data['name'] in str(response.context)

    # test that the project UpdateView did not overwrite any of the other projects
    # this is to ensure a bug doesn't creep back in
    existing_project_name = 'project_0'
    assert existing_project_name in str(response.context)

    # test the unhappy path for some of the project fields
    invalid_project_response = client.post(project_detail_url, data={**valid_form_data, **{'name': '', 'description': ''}})
    assert invalid_project_response.context['form'].errors
    
    # test the ProjectScore validation
    invalid_score_form = {**valid_form_data, **{'name': 'name', 'description': 'desc', 'core_mission_score': 0}}
    invalid_score_response = client.post(project_detail_url, data=invalid_score_form)
    assert invalid_score_response.context['score_form'].errors

    # test bad url does not exist
    bad_url = reverse('project-detail', kwargs={'pk': 1234556873459})
    bad_response = client.get(bad_url)
    assert bad_response.status_code == 404
