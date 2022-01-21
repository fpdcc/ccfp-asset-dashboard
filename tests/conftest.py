import os
import subprocess

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
