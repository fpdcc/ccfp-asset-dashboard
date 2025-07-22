from tqdm import tqdm

from django.core.management.base import BaseCommand

from asset_dashboard.models import LocalAsset


class Command(BaseCommand):
    help = "Recalculate and save geographies for all projects."

    def handle(self, *args, **options):
        # Saving an asset will trigger an update for that asset's phase and project
        projects_updated = []
        for l in tqdm(LocalAsset.objects.all()):
            if l.phase.project.id not in projects_updated:
                l.save()
                projects_updated.append(l.phase.project.id)
