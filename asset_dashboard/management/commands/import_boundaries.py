from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import GEOSGeometry

from asset_dashboard.models import Zone, FPDCCZones, FPDCCCommissionerDistricts, \
 CommissionerDistrict, FPDCCSenateDistricts, SenateDistrict, FPDCCHouseDistricts, \
 HouseDistrict

class Command(BaseCommand):
    help = 'Import zone and district boundaries from FPDCC GIS database'

    def handle(self, *args, **options):
        self.load_zones()
        self.load_districts()

    def load_zones(self):
        self.stdout.write(f'Importing {Zone} boundaries from {FPDCCZones}.')

        fpdcc_zones = FPDCCZones.objects.all()

        for z in fpdcc_zones:
            zone = Zone.objects.filter(
                name=z.zone,
            ).update(boundary=z.geom)

    def load_districts(self):
        model_pairs = [
            (FPDCCCommissionerDistricts, CommissionerDistrict),
            (FPDCCSenateDistricts, SenateDistrict),
            (FPDCCHouseDistricts, HouseDistrict)
        ]

        for remote_model, local_model in model_pairs:
            self.stdout.write(f'Importing {local_model} boundaries from {remote_model}.')

            qs = remote_model.objects.all()

            for instance in qs:
                district = local_model.objects.filter(
                    name=f'District {instance.district}',
                ).update(boundary=instance.geom)
