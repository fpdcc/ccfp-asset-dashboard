import csv
import os
from django.core.management.base import BaseCommand, CommandError
from asset_dashboard.models import DummyProject, Project

class Command(BaseCommand):
    help = 'Loads in dummy data for local development'

    def handle(self, *args, **options):

        dummy_projects = DummyProject.objects.all()

        if len(dummy_projects) == 0:
            with open('raw/simplified.csv', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                
                count = 0

                for row in reader:
                    p = DummyProject.objects.create(
                        name=row['name'],
                        project_description=row['project_description'],
                        budget=row['budget'],
                        zone=row['zone']
                    )
                    count += 1

                print(f'{count} objects saved to your local database. Happy development!')

        real_projects = Project.objects.all()

        if len(real_projects) == 0:
            with open('raw/2021CIPTablesDRAFT10.28.2020updated_GW_clean.csv', newline='') as csv_file:
                reader = csv.DictReader(csv_file)

                count = 0

                for row in reader:
                    project = Project.objects.create(
                        name=['']
                    )


# name = models.TextField()
#     description = models.TextField()
#     category = models.ForeignKey('ProjectCategory',
#                                  null=True,
#                                  on_delete=models.SET_NULL)
#     section_owner = models.ForeignKey(Section,
#                                       null=True,
#                                       on_delete=models.SET_NULL)
#     plan = models.ManyToManyField(Plan)

#     obligation = models.BooleanField(default=False)
#     phase_completion = models.BooleanField(default=False)
#     accessibility = models.BooleanField(default=False)
#     leverage_resource = models.BooleanField(default=False)