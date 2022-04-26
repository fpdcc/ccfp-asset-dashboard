from pathlib import Path
import json

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db import models

from asset_dashboard.models import Zone, CommissionerDistrict, SenateDistrict, \
 HouseDistrict


class Command(BaseCommand):
    help = 'Import zone and district boundaries from geojson files'

    def add_arguments(self, parser):
        parser.add_argument(
            'geojson_file',
        )

    def handle(self, *args, **options):
        with open(options['geojson_file']) as f:
            geojson = json.load(f)

        if 'zone' in options['geojson_file']:
            self.load_zones(geojson, options['geojson_file'])
        else:
            self.load_districts(geojson, options['geojson_file'])

    def load_zones(self, geojson: dict, file_path: str):
        self.stdout.write(f'Importing {Zone} boundaries from {file_path}.')

        for zone in geojson['features']:
            Zone.objects.filter(
                name=zone['properties']['zone'],
            ).update(boundary=GEOSGeometry(json.dumps(zone['geometry'])))

    def load_districts(self, geojson: dict, file_path: str):
        model = self._get_model(file_path)
        self.stdout.write(f'Importing {model} boundaries from {file_path}.')

        for feature in geojson['features']:
            # house & senate is 'DISTRICT_INT' and commissioner is 'District_1'
            district = feature['properties'].get('DISTRICT_INT')

            if not district:
                district = feature['properties'].get('District_1')

            model.objects.filter(
                name=f'District {district}',
            ).update(boundary=GEOSGeometry(json.dumps(feature['geometry'])))

    def _get_model(self, file_path: str) -> models.Model:
        models = {
            'state_commissioner': CommissionerDistrict,
            'state_senate': SenateDistrict,
            'state_house': HouseDistrict
        }

        file_stem = Path(file_path).stem

        return models[file_stem]
