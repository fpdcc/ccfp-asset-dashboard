import os
import subprocess
import json

import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from django.conf import settings
from django.test.utils import setup_databases

from asset_dashboard import models


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker, request):
    # Set up the default database as normal
    with django_db_blocker.unblock():
        setup_databases(verbosity=2, interactive=False, aliases=['default'])

    # Only run this when we don't want to test the GIS database
    if not bool(os.environ.get('TEST_GIS')):
        gis_db = settings.DATABASES['fp_postgis']
        test_gis_db_name = f'test_{gis_db["NAME"]}'

        # The GIS database will already exist on a remote server to which we have
        # readonly access, i.e., we aren't managing the schema through migrations.
        # Manually create a test database, instead.
        create_conn = psycopg2.connect(
            host=gis_db['HOST'],
            user=gis_db['USER'],
            password=gis_db['PASSWORD']
        )
        create_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with create_conn.cursor() as c:
            c.execute(f'DROP DATABASE IF EXISTS {test_gis_db_name}')
            c.execute(f'CREATE DATABASE {test_gis_db_name}')
            print(f'Created database "{test_gis_db_name}"')

        # "Migrate" the test database from a dump of the schema from the fpdcc
        # database. N.b., this dump does not contain any data. To update the dump,
        # load in the GIS data as documented in the README, then:
        # pg_dump -U postgres -Fc --schema-only -h localhost -p 32002 -d fpdcc > tests/sql/fpdcc_schema.dump
        fpdcc_schema = os.path.join(os.path.dirname(__file__), 'sql', 'fpdcc_schema.dump')
        cmd_args = [
            'pg_restore',
            '--username=postgres',
            '--host=fp-postgis',
            '--port=5432',
            f'--dbname={test_gis_db_name}',
            fpdcc_schema
        ]
        subprocess.run(cmd_args, stdout=subprocess.PIPE)
        print(f'Migrated database "{test_gis_db_name}"')

        # Update the name of the database in the settings, since we set up this
        # test database manually.
        settings.DATABASES['fp_postgis']['NAME'] = test_gis_db_name

        def teardown_fpdcc():
            with create_conn.cursor() as c:
                # Clean up any lingering transactions against the GIS database.
                # Not sure why they aren't closed out. Reference:
                # https://github.com/pytest-dev/pytest-django/issues/696
                c.execute(f'''
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{test_gis_db_name}'
                    AND pid <> pg_backend_pid()
                ''')

                c.execute(f'DROP DATABASE IF EXISTS {test_gis_db_name}')
                print(f'Destroyed database "{test_gis_db_name}"')

            create_conn.close()

        request.addfinalizer(teardown_fpdcc)


@pytest.fixture
def section_owner():
    """
    Creates and returns a section owner.
    """
    return models.Section.objects.create(name="Architecture")


@pytest.fixture
def project_category():
    return models.ProjectCategory.objects.create(category='land improvement', subcategory='restoration')


@pytest.fixture
def project(section_owner, project_category):
    """
    Creates and returns a single project.
    """

    class ProjectFactory():
        def build(self, **kwargs):
            project_info = {
                'name': 'Trail Maintenance',
                'description': 'Fixing trail erosion.',
                'section_owner': section_owner,
                'category': project_category,
            }

            project_info.update(kwargs)

            project = models.Project.objects.create(**project_info)
            models.ProjectScore.objects.create(project=project)
            models.Phase.objects.create(
                project=project,
                phase_type='feasibility',
                estimated_bid_quarter='Q1',
                status='in-progress'
            )

            return project

    return ProjectFactory()


@pytest.fixture
def project_list():
    """
    Creates and returns a QuerySet of all projects.
    """

    for index in range(10):
        name = f'project_{index}'
        description = f'description text for this project'
        section_owner = models.Section.objects.create(name=f'Section{index}')
        category = models.ProjectCategory.objects.create(
            category=f'category {index}',
            subcategory=f'subcategory {index}'
        )
        project = models.Project.objects.create(
            name=name,
            description=description,
            section_owner=section_owner,
            category=category
        )

        models.Phase.objects.create(project=project)
        models.ProjectScore.objects.create(project=project)

    return models.Project.objects.all()


@pytest.fixture
def districts():
    """
    Creates the different geographic districts.
    """

    for index in range(6):
        fake_district_name = f'District {index+1}'
        models.SenateDistrict.objects.create(name=fake_district_name)
        models.HouseDistrict.objects.create(name=fake_district_name)
        models.CommissionerDistrict.objects.create(name=fake_district_name)
        models.Zone.objects.create(name=f'Zone {index+1}')

    senate_districts = models.SenateDistrict.objects.all()
    house_districts = models.HouseDistrict.objects.all()
    commissioner_districts = models.CommissionerDistrict.objects.all()
    zones = models.Zone.objects.all()

    return senate_districts, house_districts, commissioner_districts, zones


@pytest.fixture
def score_weights():
    return models.ScoreWeights.objects.create(core_mission_score=0.7, operations_impact_score=0.8,
                                              sustainability_score=0.2, ease_score=0.6,
                                              geographic_distance_score=0.5, social_equity_score=0.4)

@pytest.fixture
def user():
    return models.User.objects.create_user(username='sylvie', password='lightnin')

@pytest.fixture
def nature_preserves():
    return models.NaturePreserves.objects.create(site_name="Lou Lou's Sanctuary")

@pytest.fixture
def test_geojson():
    return json.loads('{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"building_number":"100","building_comments":"Added To Fpd Databse 2016","grove_number":null,"forest":null,"commplace":null,"fpd_uid":1247,"division_name":"Salt Creek","region":0,"building_name":"Brookfield Zoo","complex":"Brookfield Zoo","building_type":"unknown","sqft":11279.761905482632,"alternate_address":null,"concession":null,"public_access":null,"support_building":null,"demolished":"no","a1_list_12":null,"ada_evaluation":null,"current_occupant":null,"building_description":"Unknown-Added From Cc Database","commissioner_district":16,"wastewater":null,"water":null,"ownership":null,"latitude":41.831582689998974,"longitude":-87.83579124652252,"managing_department":null,"improvement_year":null,"addition":null,"fpd_zone":"Central","old_address":null,"street_name_current":"GOLF ROAD","address_number_current":"3300","city_current":null,"zip_city_current":"Brookfield","zip_current":"60513","address_current":"3300 Golf Road, Brookfield, Il 60513","seasonal_closing":null,"pk":"1256"},"geometry":{"type":"Polygon","coordinates":[[[-87.83560191965763,41.831535950500836],[-87.83599323890846,41.831535950500836],[-87.83599674510782,41.83162103513153],[-87.83597896770718,41.83162144389445],[-87.83598268944739,41.83171184553104],[-87.83582143010092,41.83171555722877],[-87.83582343756666,41.831764320755944],[-87.83565389122822,41.83176822409932],[-87.83565112780272,41.83170101300551],[-87.8356330164162,41.831701428500565],[-87.83563262105326,41.83169183553792],[-87.83560304825646,41.83169251970175],[-87.83560057526238,41.831632348936054],[-87.83563540342124,41.83163154758606],[-87.8356316761104,41.831540981256694],[-87.83560215477311,41.831541662899085],[-87.83560191965763,41.831535950500836]]]}}]}')
