import os

from django.contrib.gis.geos import Polygon, MultiPolygon, Point, LineString

import pytest

from asset_dashboard import models


def get_all(model):
    """Helper function since every test gets a queryset.
    Also that the qs isn't empty."""
    if bool(os.environ.get('TEST_GIS')):
        qs = model.objects.all()
        assert qs.count() > 0
        return qs
    else:
        # skip the test if no TEST_GIS env variable
        # kinda hacky / workaround !
        # this function doesn't follow the SRP...
        pytest.skip()


@pytest.mark.django_db(databases=['fp_postgis'])
def test_buildings():
    buildings = get_all(models.Buildings)

    assert isinstance(buildings[0].geom, Polygon)

    assert buildings[0].building_number


@pytest.mark.django_db(databases=['fp_postgis'])
def test_holdings():
    holdings = get_all(models.Holdings)

    assert isinstance(holdings[0].geom, MultiPolygon)

    assert holdings[0].city_name


@pytest.mark.django_db(databases=['fp_postgis'])
def test_license_iga():
    l_iga = get_all(models.LicenseIGA)

    assert l_iga[0]
    assert l_iga[0].license_no
    assert l_iga[0].structure


@pytest.mark.django_db(databases=['fp_postgis'])
def test_mow_area_db():
    mow = get_all(models.MowAreaDB)
    assert mow[0].name
    assert mow[0].area
    assert mow[0].type


@pytest.mark.django_db(databases=['fp_postgis'])
def test_mwrd_fpd_lease():
    leases = get_all(models.MwrdFpdLease)

    assert isinstance(leases[0].geom, Polygon)
    assert leases[0].lease_end
    assert leases[0].acreage


@pytest.mark.django_db(databases=['fp_postgis'])
def test_names():
    names = get_all(models.Names)
    assert names[0].name


@pytest.mark.django_db(databases=['fp_postgis'])
def test_nature_preserves():
    nature_preserves = get_all(models.NaturePreserves)

    assert isinstance(nature_preserves[0].geom, MultiPolygon)
    assert nature_preserves[0].type
    assert nature_preserves[0].acreage


@pytest.mark.django_db(databases=['fp_postgis'])
def test_parking_entrance():
    parking_entrances = get_all(models.ParkingEntrance)

    assert isinstance(parking_entrances[0].geom, Point)


@pytest.mark.django_db(databases=['fp_postgis'])
def test_parking_entrance_info():
    parking_entrance_info = get_all(models.ParkingEntranceInfo)

    # test foreign key relationship
    assert isinstance(parking_entrance_info[0].parking_entrance, models.ParkingEntrance)

    # test index for foreign key relationship
    parking_entrance = models.ParkingEntrance.objects.all()[0]
    entrance_info = models.ParkingEntranceInfo.objects.get(parking_entrance=parking_entrance.id)
    assert parking_entrance == entrance_info.parking_entrance


@pytest.mark.django_db(databases=['fp_postgis'])
def test_parking_eval_17():
    p = get_all(models.ParkingEval17)

    assert p[0].date


@pytest.mark.django_db(databases=['fp_postgis'])
def test_parking_lots():
    parking_lots = get_all(models.ParkingLots)

    assert isinstance(parking_lots[0].geom, Polygon)
    assert parking_lots[0].id
    assert parking_lots[0].lot_surface
    assert parking_lots[0].zone


@pytest.mark.django_db(databases=['fp_postgis'])
def test_picnic_groves():
    picnic_groves = get_all(models.PicnicGroves)

    assert isinstance(picnic_groves[0].geom, Point)

    assert picnic_groves[0].grove
    assert picnic_groves[0].location

    # test picnic_grove / poi_info relationship
    assert isinstance(picnic_groves[0].poi_info, models.PoiInfo)
    picnic_groves[0].poi_info.zipmuni

    # test the picnic_area's parking_info through poi_info
    parking_info = picnic_groves[0].poi_info.parking_info
    assert parking_info
    assert isinstance(parking_info, models.ParkingEntranceInfo)
    assert parking_info.parking_entrance
    assert isinstance(parking_info.parking_entrance, models.ParkingEntrance)

    # test the picnic_area's name through poi_info
    nameid = picnic_groves[0].poi_info.nameid
    assert nameid
    assert isinstance(nameid, models.Names)


@pytest.mark.django_db(databases=['fp_postgis'])
def test_poi_amenity():
    poi_amenities = get_all(models.PoiAmenity)

    # all the fields in this table are either 1 or 0.
    # since 0 evaluates to False, cast to a string for testing.
    assert str(poi_amenities[0].no_dogs)
    assert str(poi_amenities[0].bike_parking)

    # test poi_amenity relationship with poi_info
    assert isinstance(poi_amenities[0].poi_info, models.PoiInfo)

    # test poi_info_id index
    poi_amenity = poi_amenities[0]
    poi_info_id = poi_amenity.poi_info.id

    # lookup an amenity with the poi_info_id
    amenity_by_lookup = models.PoiAmenity.objects.get(poi_info_id=poi_info_id)

    # test that the returned amentiy is the same as the original
    assert poi_amenity == amenity_by_lookup


@pytest.mark.django_db(databases=['fp_postgis'])
def test_poi_desc():
    poi_desc_qs = get_all(models.PoiDesc)

    assert poi_desc_qs[0]

    assert isinstance(poi_desc_qs[0].poi_info, models.PoiInfo)


@pytest.mark.django_db(databases=['fp_postgis'])
def test_poi_info():
    poi_info_qs = get_all(models.PoiInfo)

    poi_info = poi_info_qs[0]

    assert isinstance(poi_info.nameid, models.Names)
    assert poi_info.nameid.name

    # test parking entrance info index
    parking_connection = poi_info.parking_connection
    p = models.PoiInfo.objects.get(parking_connection=parking_connection.id)
    assert parking_connection == p.parking_connection


@pytest.mark.django_db(databases=['fp_postgis'])
def test_poi_to_trails():
    poi_to_trails_qs = get_all(models.PoiToTrails)

    poi_trail = poi_to_trails_qs[0]
    assert poi_trail

    assert isinstance(poi_trail.poi_info, models.PoiInfo)
    assert isinstance(poi_trail.trail_info, models.TrailsInfo)


@pytest.mark.django_db(databases=['fp_postgis'])
def test_points_of_interest():
    points_of_interest_qs = get_all(models.PointsOfInterest)

    poi = points_of_interest_qs[0]
    assert isinstance(poi.geom, Point)

    assert isinstance(poi.poi_info, models.PoiInfo)
    assert poi.poi_info.addr


@pytest.mark.django_db(databases=['fp_postgis'])
def test_regions():
    regions_qs = get_all(models.Regions)

    assert isinstance(regions_qs[0].geom, MultiPolygon)


@pytest.mark.django_db(databases=['fp_postgis'])
def test_signage():
    signage_qs = get_all(models.Signage)

    assert isinstance(signage_qs[0].geom, Point)


@pytest.mark.django_db(databases=['fp_postgis'])
def test_trail_substance_lu():
    trail_subsystem_qs = get_all(models.TrailSubsystemLu)

    assert trail_subsystem_qs[0].trail_subsystem_id


@pytest.mark.django_db(databases=['fp_postgis'])
def test_trails():
    trails = get_all(models.Trails)

    assert isinstance(trails[0].geom, LineString)


@pytest.mark.django_db(databases=['fp_postgis'])
def trails_amenity():
    trails_amenity_qs = get_all(models.TrailsAmenity)

    # test FK relationship
    assert isinstance(trails_amenity_qs[0].trails_info, models.TrailsInfo)


@pytest.mark.django_db(databases=['fp_postgis'])
def test_trails_desc():
    trails_desc_qs = get_all(models.TrailsDesc)

    assert trails_desc_qs[0].trail_subsystem


@pytest.mark.django_db(databases=['fp_postgis'])
def test_trails_info():
    trails_info_qs = get_all(models.TrailsInfo)

    assert trails_info_qs[0].trail_type
    assert trails_info_qs[0].trail_surface

    assert isinstance(trails_info_qs[0].trails, models.Trails)
    assert trails_info_qs[0].trails.geom


@pytest.mark.django_db(databases=['fp_postgis'])
def test_zones():
    zones = get_all(models.Zones)

    assert isinstance(zones[0].geom, MultiPolygon)
