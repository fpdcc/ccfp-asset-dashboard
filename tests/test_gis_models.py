from django.contrib.gis.geos import Polygon, MultiPolygon, Point

import pytest

from asset_dashboard import models


@pytest.mark.django_db(databases=['fp_postgis'])
def test_buildings():
    buildings = models.Buildings.objects.all()
    assert buildings.count() > 0

    assert isinstance(buildings[0].geom, Polygon)
    
    assert buildings[0].building_number

@pytest.mark.django_db(databases=['fp_postgis'])
def test_holdings():
    holdings = models.Holdings.objects.all()
    
    assert holdings.count() > 0
    
    assert isinstance(holdings[0].geom, MultiPolygon)
    
    assert holdings[0].city_name

@pytest.mark.django_db(databases=['fp_postgis'])
def test_license_iga():
    l = models.LicenseIGA.objects.all()
    
    assert l.count() > 0
    assert l[0]
    assert l[0].license_no
    assert l[0].structure

@pytest.mark.django_db(databases=['fp_postgis'])
def test_mow_area_db():
    mow = models.MowAreaDB.objects.all()
    
    assert mow.count() > 0
    assert mow[0].name
    assert mow[0].area
    assert mow[0].type

@pytest.mark.django_db(databases=['fp_postgis'])
def test_mwrd_fpd_lease():
    leases = models.MwrdFpdLease.objects.all()
    
    assert leases.count() > 0
    assert isinstance(leases[0].geom, Polygon)
    assert leases[0].lease_end
    assert leases[0].acreage

@pytest.mark.django_db(databases=['fp_postgis'])
def test_names():
    names = models.Names.objects.all()
    
    assert names.count() > 0
    assert names[0].name

@pytest.mark.django_db(databases=['fp_postgis'])
def test_nature_preserves():
    nature_preserves = models.NaturePreserves.objects.all()
    
    assert nature_preserves.count() > 0

    assert isinstance(nature_preserves[0].geom, MultiPolygon)
    assert nature_preserves[0].type
    assert nature_preserves[0].acreage

@pytest.mark.django_db(databases=['fp_postgis'])
def test_parking_entrance():
    parking_entrances = models.ParkingEntrance.objects.all()
    
    assert parking_entrances.count() > 0

    assert isinstance(parking_entrances[0].geom, Point)

@pytest.mark.django_db(databases=['fp_postgis'])
def test_parking_entrance_info():
    parking_entrance_info = models.ParkingEntranceInfo.objects.all()

    # test forieng key relationship
    assert isinstance(parking_entrance_info[0].parking_entrance, models.ParkingEntrance)

    # test index for foreign key relationship
    parking_entrance = models.ParkingEntrance.objects.all()[0]
    entrance_info = models.ParkingEntranceInfo.objects.get(parking_entrance=parking_entrance.id)
    assert parking_entrance == entrance_info.parking_entrance

@pytest.mark.django_db(databases=['fp_postgis'])
def test_parking_eval_17():
    p = models.ParkingEval17.objects.all()

    assert p.count() > 0

    assert p[0].date
    
@pytest.mark.django_db(databases=['fp_postgis'])
def test_parking_lots():
    parking_lots = models.ParkingLots.objects.all()
    
    assert parking_lots.count() > 0
    
    assert isinstance(parking_lots[0].geom, Polygon)
    assert parking_lots[0].id
    assert parking_lots[0].lot_surface
    assert parking_lots[0].zone

@pytest.mark.django_db(databases=['fp_postgis'])
def test_picnic_groves():
    picnic_groves = models.PicnicGroves.objects.all()

    assert picnic_groves.count() > 0

    assert isinstance(picnic_groves[0].geom, Point)
    
    assert picnic_groves[0].grove
    assert picnic_groves[0].location

    # test poi_info relationship
    assert isinstance(picnic_groves[0].poi_info, models.PoiInfo)
    picnic_groves[0].poi_info.zipmuni

    # test parking_info through poi_info
    parking_info = picnic_groves[0].poi_info.parking_info
    assert parking_info
    assert isinstance(parking_info, models.ParkingEntranceInfo)
    assert parking_info.parking_entrance
    assert isinstance(parking_info.parking_entrance, models.ParkingEntrance)

    # todo: can go even further with this

# TODO test the relationships to the name table

@pytest.mark.django_db(databases=['fp_postgis'])
def poi_amenity():
    ...
