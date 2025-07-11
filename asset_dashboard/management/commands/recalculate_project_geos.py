from tqdm import tqdm

from django.core.management.base import BaseCommand

from asset_dashboard.models import LocalAsset


class Command(BaseCommand):
    help = "Recalculate and save geographies for all projects."

    def handle(self, *args, **options):
        for l in tqdm(LocalAsset.objects.all()):
            l.save()
