import json
from pprint import pprint
import pytest
from rest_framework.test import force_authenticate

from asset_dashboard.endpoints import LocalAssetViewSet, AssetViewSet, PromotePhaseView, CountywideView, FundingStreamView
from asset_dashboard.models import LocalAsset, Phase, PhaseZoneDistribution, Project


@pytest.mark.django_db
def test_post_local_assets_unauthenticated(api, local_asset_request_body):
    request = api.post(
        '/local-assets/',
        json.dumps(local_asset_request_body),
        content_type='application/json'
    )

    view = LocalAssetViewSet.as_view({'post': 'create'})

    response = view(request)

    assert response.status_code == 403


@pytest.mark.django_db(databases=['default', 'fp_postgis'])
def test_post_local_assets_authenticated(api, local_asset_request_body, user, districts, socio_economic_zones):
    request = api.post(
        '/local-assets/',
        json.dumps(local_asset_request_body),
        content_type='application/json'
    )

    force_authenticate(request, user=user)

    view = LocalAssetViewSet.as_view({'post': 'create'})
    response = view(request)

    assert response.status_code == 201


def test_list_assets_unauthenticated(api, search_query):
    request = api.get('/assets/', search_query)

    view = AssetViewSet.as_view({'get': 'list'})
    response = view(request)

    assert response.status_code == 403


@pytest.mark.django_db(databases=['fp_postgis', 'default'])
def test_list_assets_authenticated(api, search_query, user, building):
    request = api.get('/assets/', search_query, format='json')

    force_authenticate(request, user)

    response = AssetViewSet.as_view({'get': 'list'})(request)

    assert response.status_code == 200


    feature_properties = response.data['features'][0]['properties']

    assert feature_properties['identifier'] == building.fpd_uid
    assert feature_properties['name'] == building.building_name


@pytest.mark.django_db
def test_promote_assets_to_new_phase(api, user,  project, signs_geojson):
    # Set up the project and phase
    prj = project.build()
    phase_a = Phase.objects.filter(project=prj)[0]
    
    # Relate the assets with the existing phase
    for feature in signs_geojson['features']:
        asset = LocalAsset.objects.create(
            phase=phase_a,
            geom=json.dumps(feature['geometry'])
        )
    
    # Create new phase so we can promote it
    phase_b = Phase.objects.create(
        project=prj,
        phase_type='design',
        estimated_bid_quarter='Q2',
        status='new'
    )
    
    form_data = {
        'old_phase_id': phase_a.id,
        'new_phase_id': phase_b.id
    }
    
    request = api.post(
        '/projects/phases/promote/assets/',
        json.dumps(form_data),
        content_type='application/json'
    )

    force_authenticate(request, user=user)

    view = PromotePhaseView.as_view()
    response = view(request)
    assert response.status_code == 201
    
    # Ensure the data for the two phases match our expectations.
    phase_a_assets = LocalAsset.objects.filter(phase=phase_a)
    assert len(phase_a_assets) == 0

    # Make sure it has all the assets that we started with
    phase_b_assets = LocalAsset.objects.filter(phase=phase_b)
    assert len(phase_b_assets) == len(signs_geojson['features'])


@pytest.mark.django_db
def test_promote_assets_to_new_phase(api, user,  project):
    # Set up the project and phase
    prj = project.build()
    phase = Phase.objects.filter(project=prj)[0]
    
    # Do the opposite of the instance's current setting
    new_countywide_setting = not prj.countywide
    
    form_data = {
        'countywide':  new_countywide_setting, 
        'phase_id': phase.id
    }
    
    request = api.post(
        '/projects/phases/assets/countywide/',
        json.dumps(form_data),
        content_type='application/json'
    )

    force_authenticate(request, user=user)
    view = CountywideView.as_view()
    response = view(request)
    assert response.status_code == 201
    
    # Ensure the data matches our expectations.
    # Reload the project.
    prj.refresh_from_db()
    assert prj.countywide == new_countywide_setting


@pytest.mark.django_db
def test_funding_stream_view(api, project, user):
    prj = project.build()
    phase = Phase.objects.filter(project=prj)[0]

    form_data = {
        'year': 2019,
        'budget': 30000,
        'actual_cost': 40000,
        'source_type': 'grants_fees_other',
        'funding_secured': True,
        'phase': phase.pk,
        'id': None,
    }

    request = api.post(
        '/projects/phases/fundingstream/',
        json.dumps(form_data),
        content_type='application/json'
    )

    force_authenticate(request, user=user)

    view = FundingStreamView.as_view()
    response = view(request)

    assert response.status_code == 201

    funding = phase.funding_streams.filter(year=2019, budget=30000, source_type='grants_fees_other')

    assert funding.count() == 1


@pytest.mark.django_db
def test_funding_stream_view_invalid_input(api, project, user):
    prj = project.build()
    phase = Phase.objects.filter(project=prj)[0]

    form_data = {
        'year': 1019,  # An invalid year
        'budget': 30000,
        'actual_cost': 40000,
        'source_type': 'grants_fees_other',
        'funding_secured': True,
        'phase': phase.pk,
        'id': None,
    }

    request = api.post(
        '/projects/phases/fundingstream/',
        json.dumps(form_data),
        content_type='application/json'
    )

    force_authenticate(request, user=user)

    view = FundingStreamView.as_view()
    response = view(request)

    assert response.status_code == 400

    funding = phase.funding_streams.filter(year=1019, budget=30000, source_type='grants_fees_other')

    assert funding.count() == 0