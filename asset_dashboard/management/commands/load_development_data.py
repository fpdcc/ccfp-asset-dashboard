import csv
import os
from django.core.management.base import BaseCommand, CommandError
from asset_dashboard.models import DummyProject, Project

class Command(BaseCommand):
    help = 'Loads in dummy data for local development'

    def handle(self, *args, **options):

        dummy_projects = DummyProject.objects.all().delete()

        with open('raw/simplified.csv', newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            for count, row in enumerate(reader):
                p = DummyProject.objects.create(
                    name=row['name'],
                    project_description=row['project_description'],
                    budget=row['budget'],
                    zone=row['zone']
                )

            print(f'{count} objects saved to your local database. Happy development!')