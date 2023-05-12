from functools import cached_property
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.gis.geos import GeometryCollection

from .models import LocalAsset, PhaseZoneDistribution, ProjectScore


class ProjectGISProcessor:
    """
    A helper class for calculating information about a Project's GIS assets.
    Intended to be used in a Django signal that is triggered whenever a LocalAsset
    is saved or deleted, when a Phase is deleted, or when a Project is deleted.

    Each Project can have zero or more Phases. Each Phase can have zero or more LocalAssets.
    Given a Phase, this class calculates various things about a Phase's GIS assets. It also
    uses the Phase's GIS assets to calculate the Project's geographic distance and
    social equity scores.

    Logic includes:
    1. Finds what CCFP zones and Illinois political districts where a phase has GIS assets.
    2. Calculates the distribution of a Phase's LocalAssets across the Forest Preserves' Zones.
    2. Calculates the proportion of area that all of the LocalAssets occur within the Zones.
        These calculations are saved as PhaseZoneDistribution objects and used to determine a
        Phase's cost by Zone.
    3. Calculates the geographic distance and social equity scores for the ProjectScore
        model based on the distribution of LocalAssets.
    """
    def __init__(self, phase):
        self.project = phase.project
        self.phase = phase

    @cached_property
    def phase_assets(self):
        return LocalAsset.objects.filter(phase=self.phase)

    @cached_property
    def phase_geometries(self) -> GeometryCollection:
        self.phase_polygons = LocalAsset.aggregate_polygons(self.phase_assets)
        self.phase_linestrings = LocalAsset.aggregate_linestrings(self.phase_assets)
        self.phase_points = LocalAsset.aggregate_points(self.phase_assets)

        geoms = (self.phase_polygons, self.phase_linestrings, self.phase_points)

        # filter out None
        filtered_geoms = tuple([geom for geom in filter(None, geoms)])

        return GeometryCollection(filtered_geoms)

    @cached_property
    def zone_distributions(self) -> dict:
        return LocalAsset.get_distribution_by_zone(self.phase_geometries)

    @cached_property
    def zone_proportions(self) -> dict:
        return PhaseZoneDistribution.calculate_zone_proportion(
            self.zone_distributions, self.phase_geometries.area
        )

    def save_phase_zone_distributions(self):
        for zone, proportion in self.zone_proportions.items():
            zone_distribution, _ = PhaseZoneDistribution.objects.get_or_create(
                phase=self.phase, zone=zone
            )

            zone_distribution.zone_distribution_proportion = proportion
            zone_distribution.save()

    def save_project_scores(self):
        ProjectScore.save_geographic_distance_scores(self.zone_proportions, self.project)
        ProjectScore.save_social_equity_score(
            self.phase_geometries,
            self.project,
            geoms=[self.phase_linestrings, self.phase_points, self.phase_polygons]
        )

    def save_project_zones(self):
        self.project.update_project_zones(self.phase_geometries)

    def save_project_districts(self):
        self.project.update_project_districts(self.phase_geometries)

    def delete_zone_distributions(self):
        return PhaseZoneDistribution.objects.filter(phase=self.phase).delete()

    def delete_project_zones(self):
        return self.project.zones.all().delete()

    def delete_project_districts(self):
        self.project.house_districts.all().delete()
        self.project.senate_districts.all().delete()
        self.project.commissioner_districts.all().delete()

    def reset_project_geo_scores(self):
        try:
            project_score = self.project.projectscore
            project_score.geographic_distance_score = 0
            project_score.social_equity_score = 0
            project_score.save()
        except ProjectScore.DoesNotExist:
            pass


@receiver([post_save, post_delete], sender="asset_dashboard.LocalAsset")
def calculate_gis(sender, instance, **kwargs):
    """
    This signal can be called whenever a LocalAsset is created or deleted,
    or when a Phase is deleted (due to the Phase/LocalAsset relationship).

    It needs to handle these cases:
    1. Measure the GIS assets whenever a new LocalAsset is saved,
        based on all of the Phase's existing assets + the new one.
    2. Recalculate the measurements whenever a LocalAsset is deleted,
        but only if there will be existing LocalAssets in the Phase.
    3. Delete all of the measurements when all of the LocalAssets are deleted.
    """

    gis_processor = ProjectGISProcessor(phase=instance.phase)

    if kwargs["signal"] == post_delete:
        assets = LocalAsset.objects.filter(phase=instance.phase)

        if assets.count() == 1 or assets.count() == 0:
            # This is the last asset for the phase (case #3).
            #
            # Go ahead and delete the PhaseZoneDistributions in case all of the assets
            # for a phase are deleted, but not the Phase.
            #
            # This also prevents an IntegrityError that happens in the deletion of the Phase,
            # when the last asset is deleted.
            gis_processor.delete_zone_distributions()
            gis_processor.delete_project_zones()
            gis_processor.delete_project_districts()
            gis_processor.reset_project_geo_scores()
            return

    # this logic will occur if it's a post_save signal, or if
    # it's a post_delete signal and there are still assets in the phase
    gis_processor.save_phase_zone_distributions()
    gis_processor.save_project_zones()
    gis_processor.save_project_districts()
    gis_processor.save_project_scores()
