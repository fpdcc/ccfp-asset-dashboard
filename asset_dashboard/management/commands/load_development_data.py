import csv
from django.core.management.base import BaseCommand
from asset_dashboard.models import DummyProject, ProjectCategory, Section, SenateDistrict, HouseDistrict, CommissionerDistrict, Zone


class Command(BaseCommand):
    help = 'Loads in dummy data for local development'

    def handle(self, *args, **options):

        # clean up all the data
        DummyProject.objects.all().delete()
        Section.objects.all().delete()
        ProjectCategory.objects.all().delete()
        SenateDistrict.objects.all().delete()
        HouseDistrict.objects.all().delete()
        CommissionerDistrict.objects.all().delete()
        Zone.objects.all().delete()

        # create dummy projects
        with open('raw/simplified.csv', newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            for count, row in enumerate(reader):
                DummyProject.objects.create(
                    name=row['name'],
                    project_description=row['project_description'],
                    budget=row['budget'],
                    zone=row['zone'],
                )

        # create project categories
        with open('raw/2021CIPTablesDRAFT10.28.2020updated_GW_clean.csv') as csv_file:
            reader = csv.DictReader(csv_file)

            for count, row in enumerate(reader):
                ProjectCategory.objects.get_or_create(category=row['category'], subcategory=row['subcategory'])

        # create section_owners
        Section.objects.create(name='Architecture')
        Section.objects.create(name='Landscaping')
        Section.objects.create(name='Civil Engineering')

        # create geographic districts
        for index in range(6):
            fake_district_name = f'District {index+1}'
            SenateDistrict.objects.create(name=fake_district_name)
            HouseDistrict.objects.create(name=fake_district_name)
            CommissionerDistrict.objects.create(name=fake_district_name)
            Zone.objects.create(name=f'Zone {index+1}')

        print('Test data saved to your local database. Happy development.')
