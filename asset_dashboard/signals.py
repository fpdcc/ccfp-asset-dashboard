from functools import cached_property
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.gis.geos import GeometryCollection

from .models import LocalAsset, PhaseZoneDistribution, ProjectScore


class ProjectGISCalculator:
    """
    A helper class for calculating GIS information for a project's GIS assets.

    Each project can have zero or more phases. Each phase can have zero or more LocalAssets.
    Given a Phase, this class calculates the distribution of LocalAssets across the Forest Preserves'
    "zones", as well as the proportion of area that each zone covers within the phase.
    These calculations are saved as PhaseZoneDistribution objects.

    This class also saves geographic distance scores and social equity scores to the ProjectScore
    model based on the distribution of LocalAssets within the phase.

    Finally, this class finds what CCFP zones and Illinois political districts where a phase has
    GIS assets.

    This class is intended to be used as a helper in a Django signal that is triggered whenever
    a LocalAsset object is saved or deleted, or when a Phase object is deleted.
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
        print('calling zone distributions', self.__dict__)
        return LocalAsset.get_distribution_by_zone(self.phase_geometries)

    @cached_property
    def zone_proportions(self) -> dict:
        print('calling zone proportions', self.__dict__)
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


@receiver([post_save, post_delete], sender="asset_dashboard.LocalAsset")
def calculate_gis(sender, instance, **kwargs):
    """
    This signal can be called whenever a local asset is created or deleted,
    or when a phase is deleted. It needs to handle these cases:

    1. Calculate the distribution whenever a new local asset is saved,
        based on all of the phase's existing assets + the new one.
    2. Recalculate the distribution whenever a local asset is deleted,
        but only if there will be existing assets in the phase.
    3. Delete all of the zone distributions when the phase is deleted.
    """

    gis_calculator = ProjectGISCalculator(phase=instance.phase)

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
            gis_calculator.delete_zone_distributions()
            return

    gis_calculator.save_phase_zone_distributions()

    # TODO how does this work upon delete
    gis_calculator.save_project_zones()
    gis_calculator.save_project_districts()
    gis_calculator.save_project_scores()
