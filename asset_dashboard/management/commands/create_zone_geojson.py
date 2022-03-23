import sys
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import serialize


from asset_dashboard.models import FPDCCZones

class Command(BaseCommand):
    help = "Convert FPDCC's zone geometries to GeoJSON."

    def handle(self, *args, **options):
        fpdcc_zones = FPDCCZones.objects.all()
        serialize('geojson',
            fpdcc_zones,
            geometry_field='geom',
            stream=sys.stdout
        )
