import json
from pprint import pprint
import pytest
from rest_framework.test import force_authenticate

from asset_dashboard.endpoints import LocalAssetViewSet, AssetViewSet


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


@pytest.mark.django_db
def test_post_local_assets_authenticated(api, local_asset_request_body, user):
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
