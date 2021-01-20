import csv
import os
from django.core.management.base import BaseCommand, CommandError
from asset_dashboard.models import DummyProject, Project, ProjectCategory, Section

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

        # create dummy projects
        with open('raw/simplified.csv', newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            for count, row in enumerate(reader):
                p = DummyProject.objects.create(
                    name=row['name'],
                    project_description=row['project_description'],
                    budget=row['budget'],
                    zone=row['zone'],
                )
                
        # create project categories
        with open('raw/2021CIPTablesDRAFT10.28.2020updated_GW_clean.csv') as csv_file:
            reader = csv.DictReader(csv_file)

            for count, row in enumerate(reader):
                category = ProjectCategory.objects.get_or_create(category=row['category'], subcategory=row['subcategory'])
        
        # create section_owners
        Section.objects.create(name='Architecture')
        Section.objects.create(name='Landscaping')
        Section.objects.create(name='Civil Engineering')

        print(f'Test data saved to your local database. Happy development.')
