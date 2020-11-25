import json
from asset_dashboard.models import Project

# i executed the code in the docker container
# so the paths/modules here might not work
with open('simplified.json') as json_file:
    data = json.load(json_file)
    
    for project in data['projects']:
        p = Project(
            name=project['name'],
            project_description=project['project_description'],
            budget=project['budget'],
            zone=project['zone']
        )

        p.save()
        
    print('data saved into the database. now dump it into a fixture.')