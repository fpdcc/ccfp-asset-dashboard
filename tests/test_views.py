import pytest
from django.urls import reverse
from asset_dashboard.models import Project, TaskFinances, ProjectScore, ProjectCategory, User
from django.forms.models import model_to_dict
import json
from django.utils.html import escape

@pytest.mark.django_db
def test_project_list_view(client, project_list, user):
    client.force_login(user=user)
    
    url = reverse('projects')
    response = client.get(url)
    assert response.status_code == 200
    assert list(project_list) == list(response.context['projects'])
    assert project_list[0] == response.context['projects'][0]


@pytest.mark.django_db
def test_project_list_json(client, project_list, user):
    client.force_login(user=user)
    
    url = reverse('project-list-json')
    response = client.get(url)
    
    assert response.status_code == 200
    response_body = json.loads(response.content)
    
    # test that the response matches all of the fixtures
    for index, project in enumerate(response_body['data']):
        assert project[0] == project_list[index].name
        
    # test the filtering/searching
    #
    # a request to filter based on "section" will have a query string like this:
    #
    #   http://localhost:8000/projects/json/?draw=2&columns[2][data]=2&columns[2][name]=section_owner
    #                           &columns[2][searchable]=true&columns[2][orderable]=true
    #                           &columns[2][search][value]=Architecture&columns[2][search][regex]=true
    #
    # that query string might contain more fields to be filtered, but for demonstration, that is a basic request.
    # 
    # when a user searches or filters in the UI,
    # a request is triggered with the query string parameters. the params are built based on user input.
    #
    # this is all handled by 
    # 1) the datatables jquery plugin on the frontend, which requests and renders a json response
    # 2) the django-datatables-view on the backend, which parses the query string and returns a json response
    # 
    # in the above example, the query string contains: columns[2][search][value]=Architecture
    # so that request gets all of the projects with the section named "Architecture".
    # 
    #
    # with that knowledge, test that a request returns what we expect based on the filtering values

    # test the section filter
    #
    # iterate through the project_list to get each project's section owner
    for project in project_list:
        section = project.section_owner
        url_with_section_params = f'/projects/json/?draw=2&columns[2][data]=2&columns[2][name]=section_owner \
                            &columns[2][searchable]=true&columns[2][orderable]=true \
                            &columns[2][search][value]={section.name}&columns[2][search][regex]=true'

        filtered_response = client.get(url_with_section_params)
        assert filtered_response.status_code == 200
        
        response_data = json.loads(filtered_response.content)
        
        # test that the response matches the fixtures
        for index, row in enumerate(response_data['data']):
            assert row[2] == section.name

    # test the filtering for a project category
    for category in ProjectCategory.objects.all():
        url_with_category_filter = f'/projects/json/?draw=3&columns[3][data]=3&columns[3][name]=category \
                                    &columns[3][searchable]=false&columns[3][orderable]=true \
                                    &columns[3][search][value]={category}&columns[3][search][regex]=true'

        filtered_category_response = client.get(url_with_category_filter)
        assert filtered_category_response.status_code == 200
        
        response_data = json.loads(filtered_category_response.content)

        for index, project in enumerate(response_data['data']):
            assert project[3] == escape(category.name)
                        
    # test that the response returns no data if data doesn't exist (effectively filtering out everything)
    nonexistent_section_name = 'nonexistent section'
    url_params_for_nonexistent_section = f'/projects/json/?draw=2&columns[2][data]=2&columns[2][name]=section_owner \
                        &columns[2][searchable]=true&columns[2][orderable]=true \
                        &columns[2][search][value]={nonexistent_section_name}&columns[2][search][regex]=true'
                        
    dataless_response = client.get(url_params_for_nonexistent_section)
    assert dataless_response.status_code == 200
    response_body = json.loads(dataless_response.content)
    assert len(response_body['data']) == 0


@pytest.mark.django_db
def test_add_project_view(client, section_owner, project_category, user):
    client.force_login(user=user)
    
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
def test_project_detail_view(client, project, project_list, section_owner, districts, project_category, score_weights, user):
    client.force_login(user=user)
    
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
        'phase': 'phase_1',
        'estimated_bid_quarter': 'Q1',
        'budget_0': 1000.00,
        'budget_1': 'USD',
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
    # TODO: These are no longer associated with the project. Update this test
    # once we implement Task management.
    # assert updated_project[0].phase == valid_form_data['phase']
    # assert updated_project[0].estimated_bid_quarter == valid_form_data['estimated_bid_quarter']
    assert updated_project[0].category_id == project_category.id
    assert updated_project[0].section_owner_id == section_owner.id
    
    # TaskFinances model
    task_finances = TaskFinances.objects.get(task__project=project)
    assert task_finances.budget.amount == valid_form_data['budget_0']
    
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


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_site(client):
    get_urls = [
        'projects',
        'project-list-json',
        'projects-by-district',
        'projects-district-json',
        'cip-planner'
    ]
    
    # request these urls
    for url in get_urls:
        response = client.get(reverse(url))
        
        # should be redirected to the login page
        assert response.status_code == 302
        assert reverse('login') in response.url

    # test that an unauthenticated user can't create a new project
    response = client.post(reverse('add-project'), data={'name': 'bad', 'description': 'data'})
    assert response.status_code == 302
    assert reverse('login') in response.url
    
    # test that an unauthenticated user can't update a project
    response = client.post(reverse('project-detail', kwargs={'pk': 1}), data={'name': 'data', 'description': 'no good'})
    assert response.status_code == 302
    assert reverse('login') in response.url


@pytest.mark.django_db
def test_login(client):
    user = {
        'username': 'test',
        'password': 'testtest'
    }
    
    test_user = User.objects.create_user(username=user['username'], password=user['password'])
    
    response = client.post(reverse('login'), user)
    assert response.status_code == 302
    assert reverse('projects') in response.url 
