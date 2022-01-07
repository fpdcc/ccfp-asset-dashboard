import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.contrib.gis.geos import GEOSGeometry

from .models import Buildings, LocalAsset


def paginated_qs(qs, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 10)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects


def search_assets(request) -> (Paginator.page, QuerySet):
    """
    Returns a paginated result and the original search result.
    """
    search_query = request.GET.get('q')
    asset_type = request.GET.get('asset-type')

    models = {
        'buildings': Buildings
    }

    # Dynamically use the GIS model from the request
    asset_model = models[asset_type]

    # Search and send back a list of search results
    # This isn't dynamic yet...
    search_results = asset_model.objects.filter(
        building_name__icontains=search_query).order_by('fpd_uid')
    paginated_search_results = paginated_qs(search_results, request)

    return paginated_search_results, search_results


def save_local_assets(data, phase):
    try:
        # By this point, the form class would've already looped over these.
        # For efficiency, would it be better to do the loop once and validate here?
        for feature in data['features']:
            # TODO: we might want to find any existing assets that intersect
            # with this feature and reconstruct it and/or delete existing asset...
            # how should that work?
            # We could maybe do it with postgis / geodjango, but if we did that
            # then we might want to move the logic from the frontend that finds
            # the intersections to make this geojson, so that logic lives together.
            local_asset, _ = LocalAsset.objects.get_or_create(
                geom=GEOSGeometry(json.dumps(feature['geometry'])),
                # TODO implement a dynamic way to use the type,
                # (like building_id or trail_id, etc)
                building_id=feature['properties']['pk'],
                phase_id=phase
            )

        return True
    except Exception as e:
        raise Exception(e)
