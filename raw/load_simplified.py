import json
import csv
from ..asset_dashboard.models import Project

with open('raw/simplified.csv', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        print(row['name'])
        print(row['project_description'])
        print(row['budget'])
        print(row['zone'])
        # p = Project.objects.create(
        #     name=row['name'],
        #     project_description=row['project_description'],
        #     budget=row['budget'],
        #     zone=row['zone']
        # )

        
    print('data saved into the database. now dump it into a fixture.')