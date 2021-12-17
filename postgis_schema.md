## Buildings
```
fpdcc-# \d "quercus"."buildings"
                                                    Table "quercus.buildings"
         Column         |          Type          | Collation | Nullable |                         Default                         
------------------------+------------------------+-----------+----------+---------------------------------------------------------
 buildings_id           | integer                |           | not null | nextval('quercus.buildings_buildings_id_seq'::regclass)
 geom                   | geometry(Polygon,3435) |           |          | 
 building_number        | character varying(10)  |           |          | 
 building_comments      | character varying(75)  |           |          | 
 grove_number           | character varying(5)   |           |          | 
 forest                 | character varying(40)  |           |          | 
 commplace              | character varying(20)  |           |          | 
 fpd_uid                | integer                |           |          | 
 division_name          | character varying(15)  |           |          | 
 region                 | integer                |           |          | 
 building_name          | character varying(100) |           |          | 
 complex                | character varying(100) |           |          | 
 building_type          | character varying(50)  |           |          | 
 sqft                   | double precision       |           |          | 
 alternate_address      | character varying(50)  |           |          | 
 concession             | character varying(10)  |           |          | 
 public_access          | character varying(5)   |           |          | 
 support_building       | character varying(5)   |           |          | 
 demolished             | character varying(5)   |           |          | 
 a1_list_12             | character varying(5)   |           |          | 
 ada_evaluation         | character varying(3)   |           |          | 
 current_occupant       | character varying(25)  |           |          | 
 building_description   | character varying(100) |           |          | 
 commissioner_district  | integer                |           |          | 
 wastewater             | character varying(20)  |           |          | 
 water                  | character varying(35)  |           |          | 
 ownership              | character varying(50)  |           |          | 
 latitude               | double precision       |           |          | 
 longitude              | double precision       |           |          | 
 managing_department    | character varying(25)  |           |          | 
 improvement_year       | character varying(25)  |           |          | 
 addition               | character varying(1)   |           |          | 
 fpd_zone               | character varying(10)  |           |          | 
 old_address            | character varying(150) |           |          | 
 street_name_current    | character varying(50)  |           |          | 
 address_number_current | character varying(10)  |           |          | 
 city_current           | character varying(30)  |           |          | 
 zip_city_current       | character varying(30)  |           |          | 
 zip_current            | character varying(5)   |           |          | 
 address_current        | character varying(150) |           |          | 
 seasonal_closing       | character varying(25)  |           |          | 
Indexes:
    "buildings_pkey" PRIMARY KEY, btree (buildings_id)
Triggers:
    buildings_history_delete_trigger AFTER DELETE ON quercus.buildings FOR EACH ROW EXECUTE FUNCTION quercus.buildings_history_delete()
    buildings_history_insert_trigger AFTER INSERT ON quercus.buildings FOR EACH ROW EXECUTE FUNCTION quercus.buildings_history_insert()
    buildings_history_update_trigger AFTER UPDATE ON quercus.buildings FOR EACH ROW EXECUTE FUNCTION quercus.buildings_history_update()
```

## Holdings
```
fpdcc-# \d "quercus"."holdings"

 survey_number                         | character varying(20)       |           |          | 
 plat_number                           | character varying(20)       |           |          | 
 tract_name                            | character varying(20)       |           |          | 
 remarks_a_index_remarks               | character varying(10)       |           |          | 
 chicago_real_estate_board_number      | character varying(10)       |           |          | 
 appraisal_per_acre_cost               | character varying(10)       |           |          | 
 improvement_appraisal                 | character varying(10)       |           |          | 
 other_appraisal                       | character varying(20)       |           |          | 
 chicago_real_estate_board_file_number | character varying(10)       |           |          | 
 remarks_b_appraisal_remarks           | character varying(10)       |           |          | 
 total_acreage_acquired                | numeric(10,3)               |           |          | 
 total_cost                            | double precision            |           |          | 
 per_acre_cost                         | double precision            |           |          | 
 acquired_by_negotiation               | integer                     |           |          | 
 acquired_by_condemnation              | integer                     |           |          | 
 condemnation_order                    | character varying(10)       |           |          | 
 date_of_judgment_order                | date                        |           |          | 
 participation_percent                 | character varying(5)        |           |          | 
 remarks_c_acquisition_remarks         | character varying(10)       |           |          | 
 title_guarantee_policy_number         | character varying(7)        |           |          | 
 torrens_certificate_number            | character varying(7)        |           |          | 
 type_of_document                      | character varying(4)        |           |          | 
 date_of_document                      | date                        |           |          | 
 document_number                       | character varying(8)        |           |          | 
 book_number                           | character varying(6)        |           |          | 
 page_number                           | character varying(4)        |           |          | 
 date_recorded                         | date                        |           |          | 
 remarks_d_document_remarks            | character varying(10)       |           |          | 
 volume_number                         | character varying(4)        |           |          | 
 item_number                           | character varying(8)        |           |          | 
 year_tax_claimed                      | character varying(4)        |           |          | 
 tax_amount_claimed                    | character varying(7)        |           |          | 
 date_injunction_was_filed             | character varying(12)       |           |          | 
 date_of_injunction_action             | date                        |           |          | 
 date_exempted                         | character varying(12)       |           |          | 
 remarks_e_tax_remarks                 | character varying(10)       |           |          | 
 status                                | character varying(50)       |           |          | 
 dissolve                              | integer                     |           |          | 
 parcel_name                           | character varying(50)       |           |          | 
 updated                               | date                        |           |          | 
 fpd_ac                                | numeric(10,3)               |           |          | 
 fpd_zone                              | character varying(10)       |           |          | 
 topogeom                              | topology.topogeometry       |           |          | 
 iga                                   | character varying(250)      |           |          | 
 iga_licensee                          | character varying(75)       |           |          | 
 iga_exhibit                           | character varying(250)      |           |          | 
 boundary_survey_corrected             | character varying(3)        |           |          | 
Indexes:
    "holdings_pkey" PRIMARY KEY, btree (holdings_id)
Triggers:
    holdings_history_delete_trigger AFTER DELETE ON quercus.holdings FOR EACH ROW EXECUTE FUNCTION quercus.holdings_history_delete()
    holdings_history_insert_trigger AFTER INSERT ON quercus.holdings FOR EACH ROW EXECUTE FUNCTION quercus.holdings_history_insert()
    holdings_history_update_trigger AFTER UPDATE ON quercus.holdings FOR EACH ROW EXECUTE FUNCTION quercus.holdings_history_update()
```



## LicenseIGA
```
fpdcc-# \d "quercus"."license_iga"
                                                  Table "quercus.license_iga"
     Column     |          Type           | Collation | Nullable |                           Default                           
----------------+-------------------------+-----------+----------+-------------------------------------------------------------
 license_iga_id | integer                 |           | not null | nextval('quercus.license_iga_license_iga_id_seq'::regclass)
 license_no     | character varying(32)   |           |          | 
 lic_type       | character varying(50)   |           |          | 
 entity         | character varying(100)  |           |          | 
 diameter       | character varying(50)   |           |          | 
 material       | character varying(50)   |           |          | 
 description    | character varying(250)  |           |          | 
 end_date       | date                    |           |          | 
 status         | character varying(50)   |           |          | 
 agreement_type | character varying(50)   |           |          | 
 geom           | geometry(Geometry,3435) |           |          | 
 plss_township  | integer                 |           |          | 
 plss_range     | integer                 |           |          | 
 plss_section   | integer                 |           |          | 
 structure      | quercus.yes_no_dom      |           |          | 
Indexes:
    "license_iga_pkey" PRIMARY KEY, btree (license_iga_id)
    "license_iga_geom_idx" gist (geom)
Triggers:
    license_iga_history_delete_trigger AFTER DELETE ON quercus.license_iga FOR EACH ROW EXECUTE FUNCTION quercus.license_iga_history_delete()
    license_iga_history_insert_trigger AFTER INSERT ON quercus.license_iga FOR EACH ROW EXECUTE FUNCTION quercus.license_iga_history_insert()
    license_iga_history_update_trigger AFTER UPDATE ON quercus.license_iga FOR EACH ROW EXECUTE FUNCTION quercus.license_iga_history_update()
```

## MowAreaDB
```
fpdcc-# \d "quercus"."mow_area_db"
                        Table "quercus.mow_area_db"
   Column   |            Type             | Collation | Nullable | Default 
------------+-----------------------------+-----------+----------+---------
 id         | integer                     |           | not null | 
 geom       | geometry(MultiPolygon,3435) |           |          | 
 filename   | character varying(80)       |           |          | 
 name       | character varying(141)      |           |          | 
 descriptio | character varying(187)      |           |          | 
 region     | character varying(50)       |           |          | 
 department | character varying(50)       |           |          | 
 type       | character varying(50)       |           |          | 
 area       | double precision            |           |          | 
 mow_freq   | character varying(50)       |           |          | 
 mow_date   | date                        |           |          | 
Indexes:
    "mow_area_db_pkey" PRIMARY KEY, btree (id)
```

## MwrdFpdLease
```
fpdcc-# \d "quercus"."mwrd_fpd_lease"
                                          Table "quercus.mwrd_fpd_lease"
   Column    |          Type          | Collation | Nullable |                      Default                       
-------------+------------------------+-----------+----------+----------------------------------------------------
 geom        | geometry(Polygon,3435) |           |          | 
 lease_id    | character varying(50)  |           |          | 
 acreage     | numeric(10,2)          |           |          | 
 notes       | character varying(254) |           |          | 
 id          | integer                |           | not null | nextval('quercus.mwrd_fpd_lease_id_seq'::regclass)
 lease_end   | date                   |           |          | 
 lease_start | date                   |           |          | 
Indexes:
    "mwrd_fpd_lease_pkey" PRIMARY KEY, btree (id)
    "mwrd_fpd_lease_geom_idx" gist (geom)
```

## Names
```
fpdcc-# \d "quercus"."names"
                                         Table "quercus.names"
 Column |          Type          | Collation | Nullable |                    Default                    
--------+------------------------+-----------+----------+-----------------------------------------------
 nameid | integer                |           | not null | nextval('quercus.names_nameid_seq'::regclass)
 name   | character varying(100) |           |          | 
Indexes:
    "names_pkey" PRIMARY KEY, btree (nameid)
    "unique_nameid_constraint" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "quercus.poi_info" CONSTRAINT "fk_poi_nameid" FOREIGN KEY (nameid) REFERENCES quercus.names(nameid) ON UPDATE CASCADE ON DELETE RESTRICT
```

## ParkingEntrance
```
fpdcc-# \d "quercus"."parking_entrance"
                                                     Table "quercus.parking_entrance"
       Column        |         Type         | Collation | Nullable |                                Default                                
---------------------+----------------------+-----------+----------+-----------------------------------------------------------------------
 geom                | geometry(Point,3435) |           |          | 
 parking_entrance_id | integer              |           | not null | nextval('quercus.parking_entrance_parking_entrance_id_seq'::regclass)
Indexes:
    "parking_entrance_pkey" PRIMARY KEY, btree (parking_entrance_id)
    "fki_pointsofinterest_parkingentrance" btree (parking_entrance_id)
    "parking_entrance_geom_idx" gist (geom)
Referenced by:
    TABLE "quercus.parking_entrance_info" CONSTRAINT "fk_parking_info_id_parking_entrance_id" FOREIGN KEY (parking_entrance_id) REFERENCES quercus.parking_entrance(parking_entrance_id) ON UPDATE CASCADE ON DELETE RESTRICT
```

## ParkingEntranceInfo
```
fpdcc-# \d "quercus"."parking_entrance_info"
                                                     Table "quercus.parking_entrance_info"
        Column         |          Type          | Collation | Nullable |                                Default                                 
-----------------------+------------------------+-----------+----------+------------------------------------------------------------------------
 parking_entrance_id   | integer                |           | not null | 
 multi_entrance        | quercus.yes_no_dom     |           |          | 
 private_lot           | quercus.yes_no_dom     |           |          | 
 lot_id                | integer                |           |          | 
 fpd_uid               | character varying(10)  |           |          | 
 parking_entrance_addr | character varying(250) |           |          | 
 trailaccess           | quercus.yes_no_dom     |           |          | 
 parking_info_id       | integer                |           | not null | nextval('quercus.parking_entrance_info_parking_info_id_seq'::regclass)
 entrance_closed       | quercus.yes_no_dom     |           |          | 
Indexes:
    "parking_entrance_info_pkey" PRIMARY KEY, btree (parking_info_id)
    "fki_parking_entrance_info_parking_entrance_id" btree (parking_entrance_id)
Foreign-key constraints:
    "fk_parking_info_id_parking_entrance_id" FOREIGN KEY (parking_entrance_id) REFERENCES quercus.parking_entrance(parking_entrance_id) ON UPDATE CASCADE ON DELETE RESTRICT
Referenced by:
    TABLE "quercus.poi_info" CONSTRAINT "fk_parking_info_id" FOREIGN KEY (parking_info_id) REFERENCES quercus.parking_entrance_info(parking_info_id) ON UPDATE CASCADE ON DELETE RESTRICT
    TABLE "quercus.poi_info" CONSTRAINT "fk_parking_info_id_for_parking_connection" FOREIGN KEY (parking_connection_id) REFERENCES quercus.parking_entrance_info(parking_info_id) ON UPDATE CASCADE ON DELETE RESTRICT
Triggers:
    parking_entrance_info_history_delete_trigger AFTER DELETE ON quercus.parking_entrance_info FOR EACH ROW EXECUTE FUNCTION quercus.parking_entrance_info_history_delete()
    parking_entrance_info_history_insert_trigger AFTER INSERT ON quercus.parking_entrance_info FOR EACH ROW EXECUTE FUNCTION quercus.parking_entrance_info_history_insert()
    parking_entrance_info_history_update_trigger AFTER UPDATE ON quercus.parking_entrance_info FOR EACH ROW EXECUTE FUNCTION quercus.parking_entrance_info_history_update()
```

## ParkingEval17
```
fpdcc-# \d "quercus"."parking_eval17"
                                                         Table "quercus.parking_eval17"
              Column              |       Type        | Collation | Nullable |                              Default                              
----------------------------------+-------------------+-----------+----------+-------------------------------------------------------------------
 parking_eval17_id                | integer           |           | not null | nextval('quercus.parking_eval17_parking_eval17_id_seq'::regclass)
 latitude                         | character varying |           |          | 
 longitude                        | character varying |           |          | 
 date                             | character varying |           |          | 
 division                         | character varying |           |          | 
 location                         | character varying |           |          | 
 grove_name                       | character varying |           |          | 
 grove_number                     | character varying |           |          | 
 permits_visitors                 | character varying |           |          | 
 parking_lot_area_sf              | character varying |           |          | 
 drive_area_sf                    | character varying |           |          | 
 paser_rating                     | character varying |           |          | 
 ramp_to_shelter                  | character varying |           |          | 
 ramp_length_feet                 | character varying |           |          | 
 ramp_paser_rating                | character varying |           |          | 
 regular_stalls                   | character varying |           |          | 
 disabled_stalls                  | character varying |           |          | 
 ramp_cuts_needed                 | character varying |           |          | 
 ada_signs                        | character varying |           |          | 
 signs_needed                     | character varying |           |          | 
 ada_compliant_stalls             | character varying |           |          | 
 striping_visible                 | character varying |           |          | 
 disabled_stalls_striping_needed  | character varying |           |          | 
 curb_gutter_type                 | character varying |           |          | 
 c_g_length_replaced              | character varying |           |          | 
 wheel_stops                      | character varying |           |          | 
 missing_wheel_stops              | character varying |           |          | 
 wheel_stops_replaced             | character varying |           |          | 
 storm_sewer_system               | character varying |           |          | 
 outlet_into                      | character varying |           |          | 
 pipe_visible                     | character varying |           |          | 
 grates_appropriate               | character varying |           |          | 
 cb_inlet_cleaning_needed         | character varying |           |          | 
 cb_inlet_adjustments_needed      | character varying |           |          | 
 cb_inlet_reconstruction_needed   | character varying |           |          | 
 low_areas_collect_water          | character varying |           |          | 
 unpaved_area_regrading_needed_sf | character varying |           |          | 
 attendance_2012                  | character varying |           |          | 
 attendance_2013                  | character varying |           |          | 
 permits_booked_2016              | character varying |           |          | 
 attendance_2016                  | character varying |           |          | 
 remarks                          | character varying |           |          | 
 photos                           | character varying |           |          | 
Indexes:
    "parking_eval17_pkey" PRIMARY KEY, btree (parking_eval17_id)
```

## ParkingLots
```
fpdcc-# \d "quercus"."parking_lots"
                                                    Table "quercus.parking_lots"
       Column        |          Type          | Collation | Nullable |                            Default                            
---------------------+------------------------+-----------+----------+---------------------------------------------------------------
 parking_lots_id     | integer                |           | not null | nextval('quercus.parking_lots_parking_lots_id_seq'::regclass)
 lot_id              | integer                |           |          | 
 zone                | character varying(25)  |           |          | 
 lot_access          | character varying(25)  |           |          | 
 parking_stalls      | integer                |           |          | 
 lot_surface         | character varying(25)  |           |          | 
 lot_part_type       | character varying(25)  |           |          | 
 closed              | quercus.yes_no_dom     |           |          | 
 comments            | character varying(250) |           |          | 
 geom                | geometry(Polygon,3435) |           |          | 
 maintained          | quercus.yes_no_dom     |           |          | 
 square_yards        | numeric(10,2)          |           |          | 
 acres               | numeric(10,2)          |           |          | 
 square_feet         | numeric(10,2)          |           |          | 
 maintained_by       | character varying(50)  |           |          | 
 maintenance_comment | character varying(250) |           |          | 
 accessible_stalls   | integer                |           |          | 
Indexes:
    "parking_lots_pkey" PRIMARY KEY, btree (parking_lots_id)
    "parking_lots_geom_idx" gist (geom)
Triggers:
    parking_lots_history_delete_trigger AFTER DELETE ON quercus.parking_lots FOR EACH ROW EXECUTE FUNCTION quercus.parking_lots_history_delete()
    parking_lots_history_insert_trigger AFTER INSERT ON quercus.parking_lots FOR EACH ROW EXECUTE FUNCTION quercus.parking_lots_history_insert()
    parking_lots_history_update_trigger AFTER UPDATE ON quercus.parking_lots FOR EACH ROW EXECUTE FUNCTION quercus.parking_lots_history_update()
    quercus_parking_lots_area_calc_trigger AFTER INSERT OR UPDATE ON quercus.parking_lots FOR EACH ROW EXECUTE FUNCTION quercus.parking_lots_calc_areas()
```

## PicnicGroves
```
fpdcc-# \d "quercus"."picnicgroves"
                                                            Table "quercus.picnicgroves"
       Column        |                  Type                  | Collation | Nullable |                           Default                            
---------------------+----------------------------------------+-----------+----------+--------------------------------------------------------------
 preserve_name       | character varying(100)                 |           |          | 
 grove               | integer                                |           |          | 
 division            | quercus.division_name_dom              |           |          | 
 capacity            | integer                                |           |          | 
 large_capacity      | quercus.yes_no_dom                     |           |          | 
 grove_type          | quercus.picnic_grove_type_dom          |           |          | 
 location            | character varying(50)                  |           |          | 
 status              | character varying(10)                  |           |          | 
 fpd_uid             | character varying(15)                  |           |          | 
 poi_info_id         | integer                                |           |          | 
 geom                | geometry(Point,3435)                   |           |          | 
 picnicgrove_id      | integer                                |           | not null | nextval('quercus.picnicgroves_picnicgrove_id_seq'::regclass)
 accessible          | quercus.bin_1_0_dom                    |           |          | 0
 parking_to_shelter  | integer                                |           |          | 
 shelter_to_bathroom | integer                                |           |          | 
 bathroom_type       | quercus.picnic_grove_bathroom_type_dom |           |          | 
Indexes:
    "picnicgroves_pkey" PRIMARY KEY, btree (picnicgrove_id)
Foreign-key constraints:
    "fk_picnicgroves_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE SET NULL
Triggers:
    picnicgroves_history_delete_trigger AFTER DELETE ON quercus.picnicgroves FOR EACH ROW EXECUTE FUNCTION quercus.picnicgroves_history_delete()
    picnicgroves_history_insert_trigger AFTER INSERT ON quercus.picnicgroves FOR EACH ROW EXECUTE FUNCTION quercus.picnicgroves_history_insert()
    picnicgroves_history_update_trigger AFTER UPDATE ON quercus.picnicgroves FOR EACH ROW EXECUTE FUNCTION quercus.picnicgroves_history_update()
```

## PoiAmenity
```
Last login: Wed Dec  1 09:08:29 on ttys006
You have new mail.
[oh-my-zsh] Would you like to update? [Y/n] m
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
~/code » cd ccfp-asset-dashboard                                                                                                                                                           sammcalilly@dm
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
~/code/ccfp-asset-dashboard(unmanaged-models*) » psql -U postgres -h localhost -p 32002                                                                                                    sammcalilly@dm
Password for user postgres: 
psql (14.0, server 12.5)
Type "help" for help.

postgres=# \c fpdcc
psql (14.0, server 12.5)
You are now connected to database "fpdcc" as user "postgres".
fpdcc=# \dt *.*
fpdcc=# \d "quercus"."trails_maintenance"
                                                        Table "quercus.trails_maintenance"
        Column         |          Type          | Collation | Nullable |                                  Default                                  
-----------------------+------------------------+-----------+----------+---------------------------------------------------------------------------
 trails_maintenance_id | integer                |           | not null | nextval('quercus.trails_maintenance_trails_maintenance_id_seq'::regclass)
 poi_info_id           | integer                |           |          | 
 iga_number            | integer                |           |          | 
 iga_doc               | character varying(250) |           |          | 
 maintained_by         | character varying(50)  |           |          | 
Indexes:
    "trails_maintenance_pkey" PRIMARY KEY, btree (trails_maintenance_id)
Foreign-key constraints:
    "trails_maintenance_poi_info_id_fkey" FOREIGN KEY (poi_info_id) REFERENCES quercus.trails_info(trail_info_id)

fpdcc=# select * from "quercus"."trails_maintenance";
 trails_maintenance_id | poi_info_id | iga_number | iga_doc | maintained_by 
-----------------------+-------------+------------+---------+---------------
(0 rows)

fpdcc=# \d "quercus"."trails_info"
fpdcc=# select trail_system from "quercus"."trails_info";
fpdcc=# select trail_system from "quercus"."trails_info";
fpdcc=# \d "quercus"."trails_info"
fpdcc=# select enum_range(null::quercus.trail_system_dom)
fpdcc-# 
fpdcc-# ^C
fpdcc=# ;
fpdcc=# select enum_range(null::quercus.trail_system_dom);
ERROR:  function enum_range(quercus.trail_system_dom) does not exist
LINE 1: select enum_range(null::quercus.trail_system_dom);
               ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
fpdcc=# \dT+ quercus.trail_system_dom
fpdcc=# \d "quercus"."trails_info"
fpdcc=# \d "quercus"."trails_info"
                                                 Table "quercus.trails_info"
       Column        |              Type              | Collation | Nullable |                    Default                     
---------------------+--------------------------------+-----------+----------+------------------------------------------------
 trail_system        | quercus.trail_system_dom       |           | not null | 
 trail_subsystem     | quercus.trail_subsystem_dom    |           | not null | 
 trail_color         | quercus.trail_color_dom        |           |          | 
 trail_surface       | quercus.trail_surface_type_dom |           |          | 
 trail_type          | quercus.trail_type_dom         |           |          | 
 trail_difficulty    | quercus.trail_difficulty_dom   |           |          | 
 regional_trail_name | character varying(50)          |           |          | 
 trail_desc          | character varying(250)         |           |          | 
 gps                 | quercus.yes_no_dom             |           |          | 
 comment             | character varying(254)         |           |          | 
 alt_name            | character varying(50)          |           |          | 
 cambr_name          | character varying(50)          |           |          | 
 on_street           | quercus.yes_no_dom             |           |          | 
 crossing_type       | quercus.crossing_type_dom      |           |          | 
 unrecognized        | quercus.yes_no_dom             |           | not null | 
 length_mi           | numeric(10,3)                  |           |          | 
 trails_id           | integer                        |           | not null | 
 off_fpdcc           | quercus.yes_no_dom             |           | not null | 
 web_trail           | quercus.yes_no_dom             |           | not null | 
 maintenance         | character varying(50)          |           |          | 
 length_ft           | numeric(10,2)                  |           |          | 
 trail_info_id       | integer                        |           | not null | nextval('quercus.trail_info_id_seq'::regclass)
 segment_type        | character varying(4)           |           |          | 
 direction           | character varying(15)          |           |          | 
 width               | numeric(4,1)                   |           |          | 
 gps_date            | date                           |           |          | 
 trail_name          | character varying(50)          |           |          | 
Indexes:
    "trails_info_pkey" PRIMARY KEY, btree (trail_info_id)
    "fki_trails_info_trails_id" btree (trails_id)
Foreign-key constraints:
    "fk_trails_id" FOREIGN KEY (trails_id) REFERENCES quercus.trails(trails_id) ON UPDATE CASCADE ON DELETE RESTRICT
Referenced by:
    TABLE "quercus.trails_amenity" CONSTRAINT "trails_amenity_trail_info_id_fkey" FOREIGN KEY (trail_info_id) REFERENCES quercus.trails_info(trail_info_id)
    TABLE "quercus.trails_maintenance" CONSTRAINT "trails_maintenance_poi_info_id_fkey" FOREIGN KEY (poi_info_id) REFERENCES quercus.trails_info(trail_info_id)
Triggers:
    trails_info_history_delete_trigger AFTER DELETE ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_delete()
    trails_info_history_insert_trigger AFTER INSERT ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_insert()
    trails_info_history_update_trigger AFTER UPDATE ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_update()

fpdcc=# \d "quercus"."trails_maintenance"
                                                        Table "quercus.trails_maintenance"
        Column         |          Type          | Collation | Nullable |                                  Default                                  
-----------------------+------------------------+-----------+----------+---------------------------------------------------------------------------
 trails_maintenance_id | integer                |           | not null | nextval('quercus.trails_maintenance_trails_maintenance_id_seq'::regclass)
 poi_info_id           | integer                |           |          | 
 iga_number            | integer                |           |          | 
 iga_doc               | character varying(250) |           |          | 
 maintained_by         | character varying(50)  |           |          | 
Indexes:
    "trails_maintenance_pkey" PRIMARY KEY, btree (trails_maintenance_id)
Foreign-key constraints:
    "trails_maintenance_poi_info_id_fkey" FOREIGN KEY (poi_info_id) REFERENCES quercus.trails_info(trail_info_id)

fpdcc=# \d "quercus"."trails_info"
                                                 Table "quercus.trails_info"
       Column        |              Type              | Collation | Nullable |                    Default                     
---------------------+--------------------------------+-----------+----------+------------------------------------------------
 trail_system        | quercus.trail_system_dom       |           | not null | 
 trail_subsystem     | quercus.trail_subsystem_dom    |           | not null | 
 trail_color         | quercus.trail_color_dom        |           |          | 
 trail_surface       | quercus.trail_surface_type_dom |           |          | 
 trail_type          | quercus.trail_type_dom         |           |          | 
 trail_difficulty    | quercus.trail_difficulty_dom   |           |          | 
 regional_trail_name | character varying(50)          |           |          | 
 trail_desc          | character varying(250)         |           |          | 
 gps                 | quercus.yes_no_dom             |           |          | 
 comment             | character varying(254)         |           |          | 
 alt_name            | character varying(50)          |           |          | 
 cambr_name          | character varying(50)          |           |          | 
 on_street           | quercus.yes_no_dom             |           |          | 
 crossing_type       | quercus.crossing_type_dom      |           |          | 
 unrecognized        | quercus.yes_no_dom             |           | not null | 
 length_mi           | numeric(10,3)                  |           |          | 
 trails_id           | integer                        |           | not null | 
 off_fpdcc           | quercus.yes_no_dom             |           | not null | 
 web_trail           | quercus.yes_no_dom             |           | not null | 
 maintenance         | character varying(50)          |           |          | 
 length_ft           | numeric(10,2)                  |           |          | 
 trail_info_id       | integer                        |           | not null | nextval('quercus.trail_info_id_seq'::regclass)
 segment_type        | character varying(4)           |           |          | 
 direction           | character varying(15)          |           |          | 
 width               | numeric(4,1)                   |           |          | 
 gps_date            | date                           |           |          | 
 trail_name          | character varying(50)          |           |          | 
Indexes:
    "trails_info_pkey" PRIMARY KEY, btree (trail_info_id)
    "fki_trails_info_trails_id" btree (trails_id)
Foreign-key constraints:
    "fk_trails_id" FOREIGN KEY (trails_id) REFERENCES quercus.trails(trails_id) ON UPDATE CASCADE ON DELETE RESTRICT
Referenced by:
    TABLE "quercus.trails_amenity" CONSTRAINT "trails_amenity_trail_info_id_fkey" FOREIGN KEY (trail_info_id) REFERENCES quercus.trails_info(trail_info_id)
    TABLE "quercus.trails_maintenance" CONSTRAINT "trails_maintenance_poi_info_id_fkey" FOREIGN KEY (poi_info_id) REFERENCES quercus.trails_info(trail_info_id)
Triggers:
    trails_info_history_delete_trigger AFTER DELETE ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_delete()
    trails_info_history_insert_trigger AFTER INSERT ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_insert()
    trails_info_history_update_trigger AFTER UPDATE ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_update()

fpdcc=# \d "quercus"."trails"
                                                Table "quercus.trails"
  Column   |           Type            | Collation | Nullable |                        Default                         
-----------+---------------------------+-----------+----------+--------------------------------------------------------
 geom      | geometry(LineString,3435) |           |          | 
 trails_id | integer                   |           | not null | nextval('quercus.trails_topo_trails_id_seq'::regclass)
 topogeom  | topology.topogeometry     |           |          | 
Indexes:
    "trails_topo_pkey" PRIMARY KEY, btree (trails_id)
    "idx_trails_geom" gist (geom)
Check constraints:
    "check_topogeom_topogeom" CHECK ((topogeom).topology_id = 18 AND (topogeom).layer_id = 1 AND (topogeom).type = 2)
Referenced by:
    TABLE "quercus.trails_info" CONSTRAINT "fk_trails_id" FOREIGN KEY (trails_id) REFERENCES quercus.trails(trails_id) ON UPDATE CASCADE ON DELETE RESTRICT

fpdcc=#  \d quercus.trails_desc
                                                    Table "quercus.trails_desc"
      Column      |            Type             | Collation | Nullable |                          Default                          
------------------+-----------------------------+-----------+----------+-----------------------------------------------------------
 trail_desc_id    | integer                     |           | not null | nextval('quercus.trail_desc_trail_desc_id_seq'::regclass)
 trail_subsystem  | quercus.trail_subsystem_dom |           | not null | 
 alt_name         | character varying(50)       |           |          | 
 trail_desc       | character varying(250)      |           |          | 
 map_link         | character varying(150)      |           |          | 
 map_link_spanish | character varying(150)      |           |          | 
 photo_link       | character varying(150)      |           |          | 
 web_note         | character varying(125)      |           |          | 
 hours1           | character varying(150)      |           |          | 
 hours2           | character varying(150)      |           |          | 
 season1          | character varying(50)       |           |          | 
 season2          | character varying(50)       |           |          | 
 special_hours    | character varying(150)      |           |          | 
 web_link         | character varying(150)      |           |          | 
Indexes:
    "trail_desc_pkey" PRIMARY KEY, btree (trail_desc_id)
Triggers:
    trails_desc_history_delete_trigger AFTER DELETE ON quercus.trails_desc FOR EACH ROW EXECUTE FUNCTION quercus.trails_desc_history_delete()
    trails_desc_history_insert_trigger AFTER INSERT ON quercus.trails_desc FOR EACH ROW EXECUTE FUNCTION quercus.trails_desc_history_insert()
    trails_desc_history_update_trigger AFTER UPDATE ON quercus.trails_desc FOR EACH ROW EXECUTE FUNCTION quercus.trails_desc_history_update()

fpdcc=# \d quercus.trails_amenity
                                                     Table "quercus.trails_amenity"
       Column        |        Type         | Collation | Nullable |                               Default                               
---------------------+---------------------+-----------+----------+---------------------------------------------------------------------
 trails_amenities_id | integer             |           | not null | nextval('quercus.trails_amenity_trails_amenities_id_seq'::regclass)
 hiking              | quercus.bin_1_0_dom |           |          | 0
 biking              | quercus.bin_1_0_dom |           |          | 0
 cross_country       | quercus.bin_1_0_dom |           |          | 0
 rollerblade         | quercus.bin_1_0_dom |           |          | 0
 snowshoe            | quercus.bin_1_0_dom |           |          | 0
 interpretive        | quercus.bin_1_0_dom |           |          | 0
 equestrian          | quercus.bin_1_0_dom |           |          | 0
 dog_leash           | quercus.bin_1_0_dom |           |          | 0
 trail_info_id       | integer             |           | not null | 
 no_dogs             | quercus.bin_1_0_dom |           |          | 0
Indexes:
    "trails_amenity_pkey" PRIMARY KEY, btree (trails_amenities_id)
Foreign-key constraints:
    "trails_amenity_trail_info_id_fkey" FOREIGN KEY (trail_info_id) REFERENCES quercus.trails_info(trail_info_id)
Triggers:
    trails_amenity_history_delete_trigger AFTER DELETE ON quercus.trails_amenity FOR EACH ROW EXECUTE FUNCTION quercus.trails_amenity_history_delete()
    trails_amenity_history_insert_trigger AFTER INSERT ON quercus.trails_amenity FOR EACH ROW EXECUTE FUNCTION quercus.trails_amenity_history_insert()
    trails_amenity_history_update_trigger AFTER UPDATE ON quercus.trails_amenity FOR EACH ROW EXECUTE FUNCTION quercus.trails_amenity_history_update()

fpdcc=# \dT+ quercus.bin_1_0_dom
                                                          List of data types
 Schema  |        Name         | Internal name | Size | Elements |  Owner   | Access privileges |             Description             
---------+---------------------+---------------+------+----------+----------+-------------------+-------------------------------------
 quercus | quercus.bin_1_0_dom | bin_1_0_dom   | 4    |          | postgres |                   | Values can only be integers 1 or 0.
(1 row)

fpdcc=# \dt "quercus"."zones"
         List of relations
 Schema  | Name  | Type  |  Owner   
---------+-------+-------+----------
 quercus | zones | table | postgres
(1 row)

fpdcc=# \d "quercus"."zones"
                                               Table "quercus.zones"
    Column    |            Type             | Collation | Nullable |                    Default                     
--------------+-----------------------------+-----------+----------+------------------------------------------------
 zone_id      | integer                     |           | not null | nextval('quercus.zones_zone_id_seq'::regclass)
 zone         | character varying(10)       |           |          | 
 abbreviation | character varying(2)        |           |          | 
 geom         | geometry(MultiPolygon,3435) |           |          | 
Indexes:
    "zones_pkey" PRIMARY KEY, btree (zone_id)

fpdcc=# \dT+ quercus
                                    List of data types
 Schema | Name | Internal name | Size | Elements | Owner | Access privileges | Description 
--------+------+---------------+------+----------+-------+-------------------+-------------
(0 rows)

fpdcc=# \dT+ quercus.*
fpdcc=# \d "quercus"."trail_subsystem_lu"
                                                Table "quercus.trail_subsystem_lu"
       Column       |            Type             | Collation | Nullable |                        Default                         
--------------------+-----------------------------+-----------+----------+--------------------------------------------------------
 trail_subsystem    | quercus.trail_subsystem_dom |           | not null | 
 trail_subsystem_id | integer                     |           | not null | nextval('quercus.trail_subsystem_lu_id_seq'::regclass)
Indexes:
    "trail_subsystem_lu_pkey" PRIMARY KEY, btree (trail_subsystem)

fpdcc=# select * from "quercus"."trail_subsystem_lu";
               trail_subsystem                | trail_subsystem_id 
----------------------------------------------+--------------------
 Burnham Greenway Trail System                |                  2
 Burnham Prairie Trail                        |                  3
 Cal-Sag Trail                                |                  5
 Centennial Trail                             |                  6
 Crabtree Nature Center Trails                |                  7
 Crabtree Trail                               |                  8
 Dan Ryan Trails                              |                  9
 Deer Grove Trails                            |                 10
 Des Plaines Trail System                     |                 11
 Horizon Farm Trails                          |                 12
 John Husar I&M Canal Trail                   |                 13
 Kickapoo Woods Trail                         |                 14
 Little Red Schoolhouse Nature Center Trails  |                 15
 Major Taylor Trail                           |                 16
 Midlothian Reservoir Trails                  |                 17
 Miller Meadow Trail                          |                 18
 North Branch Trail System                    |                 19
 Orland Grassland Trail System                |                 21
 Palos Trail System                           |                 22
 Paul Douglas Trail                           |                 23
 Perkins Woods Trails                         |                 24
 Plum Creek Trail                             |                 25
 Poplar Creek Trail System                    |                 26
 River Trail Nature Center Trails             |                 27
 Sagawau Environmental Learning Center Trails |                 28
 Sag Valley Trail System                      |                 29
 Salt Creek Trail System                      |                 30
 Sand Ridge Nature Center Trails              |                 31
 Thorn Creek Trail System                     |                 33
 Tinley Creek Trail System                    |                 34
 Trailside Museum of Natural History Trails   |                 35
 Vollmer Road Grove Loop                      |                 36
 Calumet Trail System                         |                 37
 Arie Crown Trails                            |                  1
 Busse Forest Trails                          |                  4
 Oak Forest Heritage Preserve Trails          |                 20
 Spring Lake Trails                           |                 32
(37 rows)

fpdcc=# \d "quercus"."trail_subsystem_lu"
                                                Table "quercus.trail_subsystem_lu"
       Column       |            Type             | Collation | Nullable |                        Default                         
--------------------+-----------------------------+-----------+----------+--------------------------------------------------------
 trail_subsystem    | quercus.trail_subsystem_dom |           | not null | 
 trail_subsystem_id | integer                     |           | not null | nextval('quercus.trail_subsystem_lu_id_seq'::regclass)
Indexes:
    "trail_subsystem_lu_pkey" PRIMARY KEY, btree (trail_subsystem)

fpdcc=# \d "quercus"."signage"
FATAL:  terminating connection due to administrator command
server closed the connection unexpectedly
	This probably means the server terminated abnormally
	before or while processing the request.
The connection to the server was lost. Attempting reset: Succeeded.
psql (14.0, server 12.5)
fpdcc=# \d "quercus"."signage"
                                             Table "quercus.signage"
       Column       |          Type          | Collation | Nullable |                   Default                   
--------------------+------------------------+-----------+----------+---------------------------------------------
 signage_id         | integer                |           | not null | nextval('quercus.signage_id_seq'::regclass)
 geom               | geometry(Point,3435)   |           |          | 
 type               | character varying(254) |           |          | 
 division           | character varying(254) |           |          | 
 zone               | character varying(254) |           |          | 
 preserve           | character varying(254) |           |          | 
 trail_system       | character varying(254) |           |          | 
 trail_color        | character varying(254) |           |          | 
 comment            | character varying(254) |           |          | 
 old_name           | character varying(10)  |           |          | 
 name               | character varying(50)  |           |          | 
 path               | character varying(60)  |           |          | 
 full_path          | character varying(100) |           |          | 
 latitude           | numeric(15,13)         |           |          | 
 longitude          | numeric(15,13)         |           |          | 
 poi_info_id        | integer                |           |          | 
 current_image_date | date                   |           |          | 
 sub_type           | character varying(254) |           |          | 
 trail_segment_id   | integer                |           |          | 
 status             | character varying(25)  |           |          | 
 removed            | character varying(3)   |           |          | 
 bad_image          | character varying(3)   |           |          | 
Indexes:
    "signage_pkey" PRIMARY KEY, btree (signage_id)
    "signage_gix" gist (geom)
Triggers:
    signage_history_delete_trigger AFTER DELETE ON quercus.signage FOR EACH ROW EXECUTE FUNCTION quercus.signage_history_delete()
    signage_history_insert_trigger AFTER INSERT ON quercus.signage FOR EACH ROW EXECUTE FUNCTION quercus.signage_history_insert()
    signage_history_update_trigger AFTER UPDATE ON quercus.signage FOR EACH ROW EXECUTE FUNCTION quercus.signage_history_update()

fpdcc=# \d "quercus"."regions"
                                                 Table "quercus.regions"
    Column     |            Type             | Collation | Nullable |                      Default                       
---------------+-----------------------------+-----------+----------+----------------------------------------------------
 region_id     | integer                     |           | not null | nextval('quercus.regions_region_id_seq'::regclass)
 region_number | integer                     |           |          | 
 geom          | geometry(MultiPolygon,3435) |           |          | 
Indexes:
    "regions_pkey" PRIMARY KEY, btree (region_id)

fpdcc=# \d "quercus"."pointsofinterest"
                                             Table "quercus.pointsofinterest"
       Column        |         Type         | Collation | Nullable |                       Default                        
---------------------+----------------------+-----------+----------+------------------------------------------------------
 geom                | geometry(Point,3435) |           |          | 
 pointsofinterest_id | integer              |           | not null | nextval('quercus.pointsofinterest_id_seq'::regclass)
 web_map_geom        | geometry(Point,4326) |           |          | 
 poi_info_id         | integer              |           | not null | 
Indexes:
    "pointsofinterest_pkey" PRIMARY KEY, btree (pointsofinterest_id)
    "idx_pointsofinterest_geom" gist (geom)
Foreign-key constraints:
    "fk_pointsofinterest_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
Triggers:
    pointsofinterest_history_delete_trigger AFTER DELETE ON quercus.pointsofinterest FOR EACH ROW EXECUTE FUNCTION quercus.pointsofinterest_history_delete()
    pointsofinterest_history_update_trigger AFTER UPDATE ON quercus.pointsofinterest FOR EACH ROW EXECUTE FUNCTION quercus.pointsofinterest_history_update()

fpdcc=# \d "quercus"."poi_to_trails"
                   Table "quercus.poi_to_trails"
    Column     |       Type       | Collation | Nullable | Default 
---------------+------------------+-----------+----------+---------
 distance      | double precision |           |          | 
 trail_info_id | integer          |           |          | 
 poi_info_id   | integer          |           |          | 
Indexes:
    "fki_poi_to_trails_poi_info_id" btree (poi_info_id)
    "fki_poi_to_trails_trail_info_id" btree (trail_info_id)

fpdcc=# \d "quercus"."poi_info"
fpdcc=# \d "quercus"."poi_info"
                                               Table "quercus.poi_info"
          Column          |          Type          | Collation | Nullable |                  Default                  
--------------------------+------------------------+-----------+----------+-------------------------------------------
 poi_info_id              | integer                |           | not null | nextval('quercus.poi_info_seq'::regclass)
 point_type               | character varying(50)  |           | not null | 
 addr                     | character varying(100) |           |          | 
 zip                      | character varying(5)   |           |          | 
 zipmuni                  | character varying(50)  |           |          | 
 municipality             | character varying(50)  |           |          | 
 public_access            | character varying(25)  |           |          | 
 latitude                 | numeric                |           |          | 
 longitude                | numeric                |           |          | 
 commdist                 | integer                |           |          | 
 zone_name                | character varying(10)  |           |          | 
 zonemapno                | integer                |           |          | 
 dwmapno                  | integer                |           |          | 
 nameid                   | integer                |           | not null | 
 pointsofinterest_id      | integer                |           |          | 
 fpd_uid                  | integer                |           |          | 
 web_poi                  | character varying(80)  |           |          | 
 web_street_addr          | character varying(100) |           |          | 
 web_muni_addr            | character varying(100) |           |          | 
 parking_connection_id    | integer                |           |          | 
 parking_info_id          | integer                |           |          | 
 alt_nameid               | integer                |           |          | 
 alt2_nameid              | integer                |           |          | 
 trail_info_id            | integer                |           |          | 
 poi_info_id_group        | integer                |           | not null | 
 maintenance_div          | character varying(15)  |           | not null | 
 maintenance_div_nickname | character varying(25)  |           |          | 
Indexes:
    "poi_info_pkey" PRIMARY KEY, btree (poi_info_id)
    "fki_poi_info_nameid" btree (nameid)
    "fki_poi_info_parking_connection_id" btree (parking_connection_id)
    "fki_poi_info_parking_info_id" btree (parking_info_id)
    "fki_poi_info_pointsofinterest_id" btree (pointsofinterest_id)
Foreign-key constraints:
    "fk_parking_info_id" FOREIGN KEY (parking_info_id) REFERENCES quercus.parking_entrance_info(parking_info_id) ON UPDATE CASCADE ON DELETE RESTRICT
    "fk_parking_info_id_for_parking_connection" FOREIGN KEY (parking_connection_id) REFERENCES quercus.parking_entrance_info(parking_info_id) ON UPDATE CASCADE ON DELETE RESTRICT
    "fk_poi_nameid" FOREIGN KEY (nameid) REFERENCES quercus.names(nameid) ON UPDATE CASCADE ON DELETE RESTRICT
Referenced by:
    TABLE "quercus.picnicgroves" CONSTRAINT "fk_picnicgroves_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE SET NULL
    TABLE "quercus.poi_amenity" CONSTRAINT "fk_poi_amenity_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "quercus.poi_desc" CONSTRAINT "fk_poi_desc_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "quercus.pointsofinterest" CONSTRAINT "fk_pointsofinterest_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
Triggers:
    poi_info_history_delete_trigger AFTER DELETE ON quercus.poi_info FOR EACH ROW EXECUTE FUNCTION quercus.poi_info_history_delete()
    poi_info_history_insert_trigger AFTER INSERT ON quercus.poi_info FOR EACH ROW EXECUTE FUNCTION quercus.poi_info_history_insert()
    poi_info_history_update_trigger AFTER UPDATE ON quercus.poi_info FOR EACH ROW EXECUTE FUNCTION quercus.poi_info_history_update()

fpdcc=# \d "quercus"."poi_desc"
                                                      Table "quercus.poi_desc"
          Column           |          Type           | Collation | Nullable |                        Default                        
---------------------------+-------------------------+-----------+----------+-------------------------------------------------------
 poi_info_id               | integer                 |           | not null | 
 hours1                    | character varying(150)  |           |          | 
 hours2                    | character varying(150)  |           |          | 
 phone                     | character varying(12)   |           |          | 
 description               | character varying(500)  |           |          | 
 web_link                  | character varying(150)  |           |          | 
 map_link                  | character varying(150)  |           |          | 
 map_link_spanish          | character varying(150)  |           |          | 
 vol_link                  | character varying(150)  |           |          | 
 vol_link2                 | character varying(150)  |           |          | 
 picnic_link               | character varying(150)  |           |          | 
 event_link                | character varying(150)  |           |          | 
 custom_link               | character varying(150)  |           |          | 
 season1                   | character varying(50)   |           |          | 
 season2                   | character varying(50)   |           |          | 
 special_hours             | character varying(150)  |           |          | 
 special_description       | character varying(500)  |           |          | 
 special_link              | character varying(150)  |           |          | 
 photo_link                | character varying(150)  |           |          | 
 poi_desc_id               | integer                 |           | not null | nextval('quercus.poi_desc_poi_desc_id_seq'::regclass)
 fish_map                  | character varying(150)  |           |          | 
 accessibility_description | character varying(1050) |           |          | 
Indexes:
    "poi_desc_pkey" PRIMARY KEY, btree (poi_desc_id)
    "fki_poi_desc_poi_info_id" btree (poi_info_id)
Foreign-key constraints:
    "fk_poi_desc_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
Triggers:
    poi_desc_history_delete_trigger AFTER DELETE ON quercus.poi_desc FOR EACH ROW EXECUTE FUNCTION quercus.poi_desc_history_delete()
    poi_desc_history_insert_trigger AFTER INSERT ON quercus.poi_desc FOR EACH ROW EXECUTE FUNCTION quercus.poi_desc_history_insert()
    poi_desc_history_update_trigger AFTER UPDATE ON quercus.poi_desc FOR EACH ROW EXECUTE FUNCTION quercus.poi_desc_history_update()

fpdcc=# \d "quercus"."poi_amenity"
fpdcc=# 
fpdcc=# "quercus"."poi_amenity"
fpdcc-# \d "quercus"."poi_amenity"

 canoe                    | quercus.bin_1_0_dom |           |          | 0
 comfortstation           | quercus.bin_1_0_dom |           |          | 0
 cross_country            | quercus.bin_1_0_dom |           |          | 0
 cycling                  | quercus.bin_1_0_dom |           |          | 0
 disc_golf                | quercus.bin_1_0_dom |           |          | 0
 dog_friendly             | quercus.bin_1_0_dom |           |          | 0
 dog_leash                | quercus.bin_1_0_dom |           |          | 0
 drinkingwater            | quercus.bin_1_0_dom |           |          | 0
 drone                    | quercus.bin_1_0_dom |           |          | 0
 ecological               | quercus.bin_1_0_dom |           |          | 0
 equestrian               | quercus.bin_1_0_dom |           |          | 0
 fishing                  | quercus.bin_1_0_dom |           |          | 0
 ice_fishing              | quercus.bin_1_0_dom |           |          | 0
 gas_powered              | quercus.bin_1_0_dom |           |          | 0
 golf                     | quercus.bin_1_0_dom |           |          | 0
 hiking                   | quercus.bin_1_0_dom |           |          | 0
 indoor_rental            | quercus.bin_1_0_dom |           |          | 0
 large_capacity           | quercus.bin_1_0_dom |           |          | 0
 m_airplane               | quercus.bin_1_0_dom |           |          | 0
 m_boat                   | quercus.bin_1_0_dom |           |          | 0
 nature_center            | quercus.bin_1_0_dom |           |          | 0
 natureplay               | quercus.bin_1_0_dom |           |          | 0
 no_alcohol               | quercus.bin_1_0_dom |           |          | 0
 no_parking               | quercus.bin_1_0_dom |           |          | 0
 overlook                 | quercus.bin_1_0_dom |           |          | 0
 public_building          | quercus.bin_1_0_dom |           |          | 0
 picnic_grove             | quercus.bin_1_0_dom |           |          | 0
 shelter                  | quercus.bin_1_0_dom |           |          | 0
 skating_ice              | quercus.bin_1_0_dom |           |          | 0
 skating_inline           | quercus.bin_1_0_dom |           |          | 0
 sledding                 | quercus.bin_1_0_dom |           |          | 0
 snowmobile               | quercus.bin_1_0_dom |           |          | 0
 swimming                 | quercus.bin_1_0_dom |           |          | 0
 toboggan                 | quercus.bin_1_0_dom |           |          | 0
 volunteer                | quercus.bin_1_0_dom |           |          | 0
 zip_line                 | quercus.bin_1_0_dom |           |          | 0
 poi_amenity_id           | integer             |           | not null | nextval('quercus.poi_amenity_poi_amenity_id_seq'::regclass)
 nature_preserve          | quercus.bin_1_0_dom |           |          | 0
 no_fishing               | quercus.bin_1_0_dom |           |          | 0
 driving_range            | quercus.bin_1_0_dom |           |          | 0
 pavilion                 | quercus.bin_1_0_dom |           |          | 0
 recreation_center        | quercus.bin_1_0_dom |           |          | 0
 bathroom_building_winter | quercus.bin_1_0_dom |           |          | 0
 bathroom_building_summer | quercus.bin_1_0_dom |           |          | 0
 bathroom_building_ada    | quercus.bin_1_0_dom |           |          | 0
 bathroom_portable_summer | quercus.bin_1_0_dom |           |          | 0
 bathroom_portable_winter | quercus.bin_1_0_dom |           |          | 0
 bathroom_portable_ada    | quercus.bin_1_0_dom |           |          | 0
 shower                   | quercus.bin_1_0_dom |           |          | 0
 dining_hall              | quercus.bin_1_0_dom |           |          | 0
 sanitation_station       | quercus.bin_1_0_dom |           |          | 0
 camp_store               | quercus.bin_1_0_dom |           |          | 0
 no_dogs                  | quercus.bin_1_0_dom |           |          | 0
 fitness_stairs           | quercus.bin_1_0_dom |           |          | 0
 accessible_shelter       | quercus.bin_1_0_dom |           |          | 0
 accessible_canoe         | quercus.bin_1_0_dom |           |          | 0
 accessible_boat          | quercus.bin_1_0_dom |           |          | 0
 accessible_fishing       | quercus.bin_1_0_dom |           |          | 0
 accessible_campsite      | quercus.bin_1_0_dom |           |          | 0
Indexes:
    "poi_amenity_pkey" PRIMARY KEY, btree (poi_amenity_id)
    "fki_poi_amenity_poi_info_id" btree (poi_info_id)
Foreign-key constraints:
    "fk_poi_amenity_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
Triggers:
    poi_amenity_history_delete_trigger AFTER DELETE ON quercus.poi_amenity FOR EACH ROW EXECUTE FUNCTION quercus.poi_amenity_history_delete()
    poi_amenity_history_insert_trigger AFTER INSERT ON quercus.poi_amenity FOR EACH ROW EXECUTE FUNCTION quercus.poi_amenity_history_insert()
    poi_amenity_history_update_trigger AFTER UPDATE ON quercus.poi_amenity FOR EACH ROW EXECUTE FUNCTION quercus.poi_amenity_history_update()
```

## PoiDesc
```
fpdcc=# \d "quercus"."poi_desc"
                                                      Table "quercus.poi_desc"
          Column           |          Type           | Collation | Nullable |                        Default                        
---------------------------+-------------------------+-----------+----------+-------------------------------------------------------
 poi_info_id               | integer                 |           | not null | 
 hours1                    | character varying(150)  |           |          | 
 hours2                    | character varying(150)  |           |          | 
 phone                     | character varying(12)   |           |          | 
 description               | character varying(500)  |           |          | 
 web_link                  | character varying(150)  |           |          | 
 map_link                  | character varying(150)  |           |          | 
 map_link_spanish          | character varying(150)  |           |          | 
 vol_link                  | character varying(150)  |           |          | 
 vol_link2                 | character varying(150)  |           |          | 
 picnic_link               | character varying(150)  |           |          | 
 event_link                | character varying(150)  |           |          | 
 custom_link               | character varying(150)  |           |          | 
 season1                   | character varying(50)   |           |          | 
 season2                   | character varying(50)   |           |          | 
 special_hours             | character varying(150)  |           |          | 
 special_description       | character varying(500)  |           |          | 
 special_link              | character varying(150)  |           |          | 
 photo_link                | character varying(150)  |           |          | 
 poi_desc_id               | integer                 |           | not null | nextval('quercus.poi_desc_poi_desc_id_seq'::regclass)
 fish_map                  | character varying(150)  |           |          | 
 accessibility_description | character varying(1050) |           |          | 
Indexes:
    "poi_desc_pkey" PRIMARY KEY, btree (poi_desc_id)
    "fki_poi_desc_poi_info_id" btree (poi_info_id)
Foreign-key constraints:
    "fk_poi_desc_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
Triggers:
    poi_desc_history_delete_trigger AFTER DELETE ON quercus.poi_desc FOR EACH ROW EXECUTE FUNCTION quercus.poi_desc_history_delete()
    poi_desc_history_insert_trigger AFTER INSERT ON quercus.poi_desc FOR EACH ROW EXECUTE FUNCTION quercus.poi_desc_history_insert()
    poi_desc_history_update_trigger AFTER UPDATE ON quercus.poi_desc FOR EACH ROW EXECUTE FUNCTION quercus.poi_desc_history_update()
```

## PoiInfo
```
fpdcc=# \d "quercus"."poi_info"

                                               Table "quercus.poi_info"
          Column          |          Type          | Collation | Nullable |                  Default                  
--------------------------+------------------------+-----------+----------+-------------------------------------------
 poi_info_id              | integer                |           | not null | nextval('quercus.poi_info_seq'::regclass)
 point_type               | character varying(50)  |           | not null | 
 addr                     | character varying(100) |           |          | 
 zip                      | character varying(5)   |           |          | 
 zipmuni                  | character varying(50)  |           |          | 
 municipality             | character varying(50)  |           |          | 
 public_access            | character varying(25)  |           |          | 
 latitude                 | numeric                |           |          | 
 longitude                | numeric                |           |          | 
 commdist                 | integer                |           |          | 
 zone_name                | character varying(10)  |           |          | 
 zonemapno                | integer                |           |          | 
 dwmapno                  | integer                |           |          | 
 nameid                   | integer                |           | not null | 
 pointsofinterest_id      | integer                |           |          | 
 fpd_uid                  | integer                |           |          | 
 web_poi                  | character varying(80)  |           |          | 
 web_street_addr          | character varying(100) |           |          | 
 web_muni_addr            | character varying(100) |           |          | 
 parking_connection_id    | integer                |           |          | 
 parking_info_id          | integer                |           |          | 
 alt_nameid               | integer                |           |          | 
 alt2_nameid              | integer                |           |          | 
 trail_info_id            | integer                |           |          | 
 poi_info_id_group        | integer                |           | not null | 
 maintenance_div          | character varying(15)  |           | not null | 
 maintenance_div_nickname | character varying(25)  |           |          | 
Indexes:
    "poi_info_pkey" PRIMARY KEY, btree (poi_info_id)
    "fki_poi_info_nameid" btree (nameid)
    "fki_poi_info_parking_connection_id" btree (parking_connection_id)
    "fki_poi_info_parking_info_id" btree (parking_info_id)
    "fki_poi_info_pointsofinterest_id" btree (pointsofinterest_id)
Foreign-key constraints:
    "fk_parking_info_id" FOREIGN KEY (parking_info_id) REFERENCES quercus.parking_entrance_info(parking_info_id) ON UPDATE CASCADE ON DELETE RESTRICT
    "fk_parking_info_id_for_parking_connection" FOREIGN KEY (parking_connection_id) REFERENCES quercus.parking_entrance_info(parking_info_id) ON UPDATE CASCADE ON DELETE RESTRICT
    "fk_poi_nameid" FOREIGN KEY (nameid) REFERENCES quercus.names(nameid) ON UPDATE CASCADE ON DELETE RESTRICT
Referenced by:
    TABLE "quercus.picnicgroves" CONSTRAINT "fk_picnicgroves_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE SET NULL
    TABLE "quercus.poi_amenity" CONSTRAINT "fk_poi_amenity_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "quercus.poi_desc" CONSTRAINT "fk_poi_desc_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "quercus.pointsofinterest" CONSTRAINT "fk_pointsofinterest_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
Triggers:
    poi_info_history_delete_trigger AFTER DELETE ON quercus.poi_info FOR EACH ROW EXECUTE FUNCTION quercus.poi_info_history_delete()
    poi_info_history_insert_trigger AFTER INSERT ON quercus.poi_info FOR EACH ROW EXECUTE FUNCTION quercus.poi_info_history_insert()
    poi_info_history_update_trigger AFTER UPDATE ON quercus.poi_info FOR EACH ROW EXECUTE FUNCTION quercus.poi_info_history_update()
```

## PoiToTrails
```
fpdcc=# \d "quercus"."poi_to_trails"
                   Table "quercus.poi_to_trails"
    Column     |       Type       | Collation | Nullable | Default 
---------------+------------------+-----------+----------+---------
 distance      | double precision |           |          | 
 trail_info_id | integer          |           |          | 
 poi_info_id   | integer          |           |          | 
Indexes:
    "fki_poi_to_trails_poi_info_id" btree (poi_info_id)
    "fki_poi_to_trails_trail_info_id" btree (trail_info_id)
```

## PointsOfInterest
```
fpdcc=# \d "quercus"."pointsofinterest"
                                             Table "quercus.pointsofinterest"
       Column        |         Type         | Collation | Nullable |                       Default                        
---------------------+----------------------+-----------+----------+------------------------------------------------------
 geom                | geometry(Point,3435) |           |          | 
 pointsofinterest_id | integer              |           | not null | nextval('quercus.pointsofinterest_id_seq'::regclass)
 web_map_geom        | geometry(Point,4326) |           |          | 
 poi_info_id         | integer              |           | not null | 
Indexes:
    "pointsofinterest_pkey" PRIMARY KEY, btree (pointsofinterest_id)
    "idx_pointsofinterest_geom" gist (geom)
Foreign-key constraints:
    "fk_pointsofinterest_poi_info_id" FOREIGN KEY (poi_info_id) REFERENCES quercus.poi_info(poi_info_id) ON UPDATE CASCADE ON DELETE CASCADE
Triggers:
    pointsofinterest_history_delete_trigger AFTER DELETE ON quercus.pointsofinterest FOR EACH ROW EXECUTE FUNCTION quercus.pointsofinterest_history_delete()
    pointsofinterest_history_update_trigger AFTER UPDATE ON quercus.pointsofinterest FOR EACH ROW EXECUTE FUNCTION quercus.pointsofinterest_history_update()
```

## Regions
```
fpdcc=# \d "quercus"."regions"
                                                 Table "quercus.regions"
    Column     |            Type             | Collation | Nullable |                      Default                       
---------------+-----------------------------+-----------+----------+----------------------------------------------------
 region_id     | integer                     |           | not null | nextval('quercus.regions_region_id_seq'::regclass)
 region_number | integer                     |           |          | 
 geom          | geometry(MultiPolygon,3435) |           |          | 
Indexes:
    "regions_pkey" PRIMARY KEY, btree (region_id)
```

## Signage
```
fpdcc=# \d "quercus"."signage"
                                             Table "quercus.signage"
       Column       |          Type          | Collation | Nullable |                   Default                   
--------------------+------------------------+-----------+----------+---------------------------------------------
 signage_id         | integer                |           | not null | nextval('quercus.signage_id_seq'::regclass)
 geom               | geometry(Point,3435)   |           |          | 
 type               | character varying(254) |           |          | 
 division           | character varying(254) |           |          | 
 zone               | character varying(254) |           |          | 
 preserve           | character varying(254) |           |          | 
 trail_system       | character varying(254) |           |          | 
 trail_color        | character varying(254) |           |          | 
 comment            | character varying(254) |           |          | 
 old_name           | character varying(10)  |           |          | 
 name               | character varying(50)  |           |          | 
 path               | character varying(60)  |           |          | 
 full_path          | character varying(100) |           |          | 
 latitude           | numeric(15,13)         |           |          | 
 longitude          | numeric(15,13)         |           |          | 
 poi_info_id        | integer                |           |          | 
 current_image_date | date                   |           |          | 
 sub_type           | character varying(254) |           |          | 
 trail_segment_id   | integer                |           |          | 
 status             | character varying(25)  |           |          | 
 removed            | character varying(3)   |           |          | 
 bad_image          | character varying(3)   |           |          | 
Indexes:
    "signage_pkey" PRIMARY KEY, btree (signage_id)
    "signage_gix" gist (geom)
Triggers:
    signage_history_delete_trigger AFTER DELETE ON quercus.signage FOR EACH ROW EXECUTE FUNCTION quercus.signage_history_delete()
    signage_history_insert_trigger AFTER INSERT ON quercus.signage FOR EACH ROW EXECUTE FUNCTION quercus.signage_history_insert()
    signage_history_update_trigger AFTER UPDATE ON quercus.signage FOR EACH ROW EXECUTE FUNCTION quercus.signage_history_update()
```


## TrailSubsystemLu
```
fpdcc=# \d "quercus"."trail_subsystem_lu"
                                                Table "quercus.trail_subsystem_lu"
       Column       |            Type             | Collation | Nullable |                        Default                         
--------------------+-----------------------------+-----------+----------+--------------------------------------------------------
 trail_subsystem    | quercus.trail_subsystem_dom |           | not null | 
 trail_subsystem_id | integer                     |           | not null | nextval('quercus.trail_subsystem_lu_id_seq'::regclass)
Indexes:
    "trail_subsystem_lu_pkey" PRIMARY KEY, btree (trail_subsystem)
```


## Trails
```
fpdcc=# \d "quercus"."trails"
                                                Table "quercus.trails"
  Column   |           Type            | Collation | Nullable |                        Default                         
-----------+---------------------------+-----------+----------+--------------------------------------------------------
 geom      | geometry(LineString,3435) |           |          | 
 trails_id | integer                   |           | not null | nextval('quercus.trails_topo_trails_id_seq'::regclass)
 topogeom  | topology.topogeometry     |           |          | 
Indexes:
    "trails_topo_pkey" PRIMARY KEY, btree (trails_id)
    "idx_trails_geom" gist (geom)
Check constraints:
    "check_topogeom_topogeom" CHECK ((topogeom).topology_id = 18 AND (topogeom).layer_id = 1 AND (topogeom).type = 2)
Referenced by:
    TABLE "quercus.trails_info" CONSTRAINT "fk_trails_id" FOREIGN KEY (trails_id) REFERENCES quercus.trails(trails_id) ON UPDATE CASCADE ON DELETE RESTRICT
```

## TrailsAmenity
```
fpdcc=# \d quercus.trails_amenity
                                                     Table "quercus.trails_amenity"
       Column        |        Type         | Collation | Nullable |                               Default                               
---------------------+---------------------+-----------+----------+---------------------------------------------------------------------
 trails_amenities_id | integer             |           | not null | nextval('quercus.trails_amenity_trails_amenities_id_seq'::regclass)
 hiking              | quercus.bin_1_0_dom |           |          | 0
 biking              | quercus.bin_1_0_dom |           |          | 0
 cross_country       | quercus.bin_1_0_dom |           |          | 0
 rollerblade         | quercus.bin_1_0_dom |           |          | 0
 snowshoe            | quercus.bin_1_0_dom |           |          | 0
 interpretive        | quercus.bin_1_0_dom |           |          | 0
 equestrian          | quercus.bin_1_0_dom |           |          | 0
 dog_leash           | quercus.bin_1_0_dom |           |          | 0
 trail_info_id       | integer             |           | not null | 
 no_dogs             | quercus.bin_1_0_dom |           |          | 0
Indexes:
    "trails_amenity_pkey" PRIMARY KEY, btree (trails_amenities_id)
Foreign-key constraints:
    "trails_amenity_trail_info_id_fkey" FOREIGN KEY (trail_info_id) REFERENCES quercus.trails_info(trail_info_id)
Triggers:
    trails_amenity_history_delete_trigger AFTER DELETE ON quercus.trails_amenity FOR EACH ROW EXECUTE FUNCTION quercus.trails_amenity_history_delete()
    trails_amenity_history_insert_trigger AFTER INSERT ON quercus.trails_amenity FOR EACH ROW EXECUTE FUNCTION quercus.trails_amenity_history_insert()
    trails_amenity_history_update_trigger AFTER UPDATE ON quercus.trails_amenity FOR EACH ROW EXECUTE FUNCTION quercus.trails_amenity_history_update()

fpdcc=# \dT+ quercus.bin_1_0_dom
                                                          List of data types
 Schema  |        Name         | Internal name | Size | Elements |  Owner   | Access privileges |             Description             
---------+---------------------+---------------+------+----------+----------+-------------------+-------------------------------------
 quercus | quercus.bin_1_0_dom | bin_1_0_dom   | 4    |          | postgres |                   | Values can only be integers 1 or 0.
(1 row)
```

## TrailsDesc
```
fpdcc=#  \d quercus.trails_desc
                                                    Table "quercus.trails_desc"
      Column      |            Type             | Collation | Nullable |                          Default                          
------------------+-----------------------------+-----------+----------+-----------------------------------------------------------
 trail_desc_id    | integer                     |           | not null | nextval('quercus.trail_desc_trail_desc_id_seq'::regclass)
 trail_subsystem  | quercus.trail_subsystem_dom |           | not null | 
 alt_name         | character varying(50)       |           |          | 
 trail_desc       | character varying(250)      |           |          | 
 map_link         | character varying(150)      |           |          | 
 map_link_spanish | character varying(150)      |           |          | 
 photo_link       | character varying(150)      |           |          | 
 web_note         | character varying(125)      |           |          | 
 hours1           | character varying(150)      |           |          | 
 hours2           | character varying(150)      |           |          | 
 season1          | character varying(50)       |           |          | 
 season2          | character varying(50)       |           |          | 
 special_hours    | character varying(150)      |           |          | 
 web_link         | character varying(150)      |           |          | 
Indexes:
    "trail_desc_pkey" PRIMARY KEY, btree (trail_desc_id)
Triggers:
    trails_desc_history_delete_trigger AFTER DELETE ON quercus.trails_desc FOR EACH ROW EXECUTE FUNCTION quercus.trails_desc_history_delete()
    trails_desc_history_insert_trigger AFTER INSERT ON quercus.trails_desc FOR EACH ROW EXECUTE FUNCTION quercus.trails_desc_history_insert()
    trails_desc_history_update_trigger AFTER UPDATE ON quercus.trails_desc FOR EACH ROW EXECUTE FUNCTION quercus.trails_desc_history_update()
```

## TrailsInfo
```
fpdcc=# \d "quercus"."trails_info"
                                                 Table "quercus.trails_info"
       Column        |              Type              | Collation | Nullable |                    Default                     
---------------------+--------------------------------+-----------+----------+------------------------------------------------
 trail_system        | quercus.trail_system_dom       |           | not null | 
 trail_subsystem     | quercus.trail_subsystem_dom    |           | not null | 
 trail_color         | quercus.trail_color_dom        |           |          | 
 trail_surface       | quercus.trail_surface_type_dom |           |          | 
 trail_type          | quercus.trail_type_dom         |           |          | 
 trail_difficulty    | quercus.trail_difficulty_dom   |           |          | 
 regional_trail_name | character varying(50)          |           |          | 
 trail_desc          | character varying(250)         |           |          | 
 gps                 | quercus.yes_no_dom             |           |          | 
 comment             | character varying(254)         |           |          | 
 alt_name            | character varying(50)          |           |          | 
 cambr_name          | character varying(50)          |           |          | 
 on_street           | quercus.yes_no_dom             |           |          | 
 crossing_type       | quercus.crossing_type_dom      |           |          | 
 unrecognized        | quercus.yes_no_dom             |           | not null | 
 length_mi           | numeric(10,3)                  |           |          | 
 trails_id           | integer                        |           | not null | 
 off_fpdcc           | quercus.yes_no_dom             |           | not null | 
 web_trail           | quercus.yes_no_dom             |           | not null | 
 maintenance         | character varying(50)          |           |          | 
 length_ft           | numeric(10,2)                  |           |          | 
 trail_info_id       | integer                        |           | not null | nextval('quercus.trail_info_id_seq'::regclass)
 segment_type        | character varying(4)           |           |          | 
 direction           | character varying(15)          |           |          | 
 width               | numeric(4,1)                   |           |          | 
 gps_date            | date                           |           |          | 
 trail_name          | character varying(50)          |           |          | 
Indexes:
    "trails_info_pkey" PRIMARY KEY, btree (trail_info_id)
    "fki_trails_info_trails_id" btree (trails_id)
Foreign-key constraints:
    "fk_trails_id" FOREIGN KEY (trails_id) REFERENCES quercus.trails(trails_id) ON UPDATE CASCADE ON DELETE RESTRICT
Referenced by:
    TABLE "quercus.trails_amenity" CONSTRAINT "trails_amenity_trail_info_id_fkey" FOREIGN KEY (trail_info_id) REFERENCES quercus.trails_info(trail_info_id)
    TABLE "quercus.trails_maintenance" CONSTRAINT "trails_maintenance_poi_info_id_fkey" FOREIGN KEY (poi_info_id) REFERENCES quercus.trails_info(trail_info_id)
Triggers:
    trails_info_history_delete_trigger AFTER DELETE ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_delete()
    trails_info_history_insert_trigger AFTER INSERT ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_insert()
    trails_info_history_update_trigger AFTER UPDATE ON quercus.trails_info FOR EACH ROW EXECUTE FUNCTION quercus.trails_info_history_update()
```

## TrailsMaintenance
```
fpdcc=# \d "quercus"."trails_maintenance"
                                                        Table "quercus.trails_maintenance"
        Column         |          Type          | Collation | Nullable |                                  Default                                  
-----------------------+------------------------+-----------+----------+---------------------------------------------------------------------------
 trails_maintenance_id | integer                |           | not null | nextval('quercus.trails_maintenance_trails_maintenance_id_seq'::regclass)
 poi_info_id           | integer                |           |          | 
 iga_number            | integer                |           |          | 
 iga_doc               | character varying(250) |           |          | 
 maintained_by         | character varying(50)  |           |          | 
Indexes:
    "trails_maintenance_pkey" PRIMARY KEY, btree (trails_maintenance_id)
Foreign-key constraints:
    "trails_maintenance_poi_info_id_fkey" FOREIGN KEY (poi_info_id) REFERENCES quercus.trails_info(trail_info_id)

fpdcc=# select * from "quercus"."trails_maintenance";
 trails_maintenance_id | poi_info_id | iga_number | iga_doc | maintained_by 
-----------------------+-------------+------------+---------+---------------
(0 rows)
```

## Zones
```
fpdcc=# \d "quercus"."zones"
                                               Table "quercus.zones"
    Column    |            Type             | Collation | Nullable |                    Default                     
--------------+-----------------------------+-----------+----------+------------------------------------------------
 zone_id      | integer                     |           | not null | nextval('quercus.zones_zone_id_seq'::regclass)
 zone         | character varying(10)       |           |          | 
 abbreviation | character varying(2)        |           |          | 
 geom         | geometry(MultiPolygon,3435) |           |          | 
Indexes:
    "zones_pkey" PRIMARY KEY, btree (zone_id)
```

## Column types with enums

### Quercus
```
fpdcc=# \dT+ quercus.*
                       List of data types
 Schema  |                  Name                  |         Internal name          | Size | Elements |  Owner   | Access privileges |                                                                                    Description                                                                                    
---------+----------------------------------------+--------------------------------+------+----------+----------+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 quercus | quercus.bin_1_0_dom                    | bin_1_0_dom                    | 4    |          | postgres |                   | Values can only be integers 1 or 0.
 quercus | quercus.crossing_type_dom              | crossing_type_dom              | var  |          | postgres |                   | Values can only be bridge, none, railroad, road, underpass
 quercus | quercus.division_name_dom              | division_name_dom              | var  |          | postgres |                   | Values can only be a proper Division name - Calumet,Des Plaines,Indian Boundary,North Branch,Northwest,Palos,Poplar Creek,Sag Valley,Salt Creek,Skokie,Thorn Creek,Tinley Creek
 quercus | quercus.picnic_grove_bathroom_type_dom | picnic_grove_bathroom_type_dom | var  |          | postgres |                   | Values can only be indoor, or portable
 quercus | quercus.picnic_grove_status_dom        | picnic_grove_status_dom        | var  |          | postgres |                   | Values can only be - active or inactive
 quercus | quercus.picnic_grove_type_dom          | picnic_grove_type_dom          | var  |          | postgres |                   | Values can only be - shelter or no shelter
 quercus | quercus.trail_color_dom                | trail_color_dom                | var  |          | postgres |                   | Values can only be orange, olive, tan, blue, purple, brown, yellow, green, red, black
 quercus | quercus.trail_difficulty_dom           | trail_difficulty_dom           | var  |          | postgres |                   | Values can only be easy, intermediate, advanced, expert
 quercus | quercus.trail_subsystem_dom            | trail_subsystem_dom            | var  |          | postgres |                   | Values must be within trail_subsystem_constraint. See quercus.trail_subsystem_lu for a list of values
 quercus | quercus.trail_surface_type_dom         | trail_surface_type_dom         | var  |          | postgres |                   | Values can only be asphault, cement, crushed granite, crushed limestone, dirt, flagstone, grass, gravel, gravel/dirt, lawn, mowed, natural, natural surface, soil, stone, unknown
 quercus | quercus.trail_system_dom               | trail_system_dom               | var  |          | postgres |                   | Values can only be palos, calumet, northwest, north branch, salt creek, thorn creek, tinley creek, poplar creek, skokie, sag valley, indian boundary, des plaines
 quercus | quercus.trail_type_dom                 | trail_type_dom                 | var  |          | postgres |                   | 
 quercus | quercus.yes_no_dom                     | yes_no_dom                     | var  |          | postgres |                   | Values can only be  yes or no
(13 rows)

```
