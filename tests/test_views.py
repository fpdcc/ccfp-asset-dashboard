import pytest
from django.urls import reverse
from asset_dashboard.models import Project, ProjectScore
from django.forms.models import model_to_dict

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
        assert invalid_response.status_code == 400

def create_formset_data(formset, new_form_data=None):
    """
    Creates formset data from a response's context.
    See https://stackoverflow.com/questions/1630754/django-formset-unit-test/64354805.
    """
    if new_form_data is None:
        new_form_data = []

    # setup the formset
    form_data = {}
    prefix_template = formset.empty_form.prefix
    form_data_list = formset.initial or []
    form_data_list.extend(new_form_data)
    
    # add management fields to the form_data
    management_data = formset.management_form.initial
    management_data['TOTAL_FORMS'] = len(form_data_list)
    for key, value in management_data.items():
        prefix = prefix_template.replace('__prefix__', '')
        form_data[prefix + key] = value

    # populate each form within the formset
    for index, data in enumerate(form_data_list):
        for key, value in data.items():
            prefix = prefix_template.replace('__prefix__', f'{index}-')
            form_data[prefix + key] = value
    
    return form_data
    

@pytest.mark.django_db
def test_project_detail_view(client, project, project_list, section_owner):
    project_detail_url = reverse('project-detail', kwargs={'pk': project.pk})
    response = client.get(project_detail_url)
    assert response.status_code == 200

    project_from_response = response.context['project']
    project_score_from_response = response.context['project'].projectscore
    senate_district_from_response = response.context['senate_district_formset']
    house_district_from_response = response.context['house_district_formset']
    commissioner_district_from_response = response.context['commissioner_district_formset']
    zones_from_response = response.context['zone_formset']

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
        'core_mission_score': 2
    })
    
    # populate the fields for all of the formsets
    senate_district_formset = create_formset_data(senate_district_from_response, new_form_data=[{'name': 'district 1'}])
    valid_form_data.update(senate_district_formset)
    
    house_district_formset = create_formset_data(house_district_from_response, new_form_data=[{'name': 'district 2'}])
    valid_form_data.update(house_district_formset)
    
    commissioner_district_formset = create_formset_data(commissioner_district_from_response, new_form_data=[{'name': 'district 11'}])
    valid_form_data.update(commissioner_district_formset)
    
    zone_formset = create_formset_data(zones_from_response, new_form_data=[{'name': 'zone 2'}])
    valid_form_data.update(zone_formset)

    # test the form submission
    successful_response = client.post(project_detail_url, data=valid_form_data)
    assert successful_response.status_code == 302

    # test that the update form saved the project with correct data
    updated_project = Project.objects.filter(name=valid_form_data['name'])
    assert updated_project[0].name == valid_form_data['name']
    assert updated_project[0].description == valid_form_data['description']

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

    # test the unhappy path
    invalid_form_data = [
        valid_form_data.update({'name': '', 'description': ''}),
        valid_form_data.update({'name': ''}),
        valid_form_data.update({'description': ''}),
        valid_form_data.update({'name': 'name without description'}),
        valid_form_data.update({'description': 'description without name'}),
        valid_form_data.update({'core_mission_score': 0}), # ensure the ProjectScore form validation works
    ]

    for form_data in invalid_form_data:
        invalid_response = client.post(project_detail_url, data=form_data)
        assert invalid_response.context['form'].errors

    # test bad url does not exist
    bad_url = reverse('project-detail', kwargs={'pk': 1234556873459})
    bad_response = client.get(bad_url)
    assert bad_response.status_code == 404
