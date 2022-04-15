from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models import Union
from asset_dashboard.models import Zone, LocalAsset, Phase


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        phase = Phase.objects.get(id=1)
        zones = Zone.objects.all()
        phase_assets = LocalAsset.objects.filter(phase=phase)
        
        phase_polygons = self.aggregate_polygons(phase_assets)
        phase_linestrings = self.aggregate_linestrings(phase_assets)
        phase_points = self.aggregate_points(phase_assets)

        total_phase_calculations = {
            'area': phase_polygons.area,
            'length': phase_linestrings.length,
            'point_count': phase_points.count()
        }
        
        zone_calulations = {}

        for zone in zones:
            if zone.boundary:
                print('zone.name', zone.name)
                poly_intersection = phase_polygons.intersection(zone.boundary)
                zone_calulations[zone.name] = {
                    'area': zone.boundary.intersection(phase_polygons).area,
                    'length': zone.boundary.intersection(phase_linestrings).length,
                    'point_count': self.get_point_count_in_zone(zone, phase_points)
                }

        from pprint import pprint
        pprint(zone_calulations)
        pprint(total_phase_calculations)
    
    def aggregate_polygons(self, qs):
        assets = qs.extra(where=["""
                                    geometrytype(geom) LIKE 'POLYGON' 
                                        OR geometrytype(geom) LIKE 'MULTIPOLYGON'
                                 """]).aggregate(Union('geom'))

        return assets['geom__union']
    
    def aggregate_linestrings(self, qs):
        assets = qs.extra(
            where=["""
                    geometrytype(geom) LIKE 'LINESTRING' 
                        OR geometrytype(geom) LIKE 'MULTILINESTRING'
                   """]).aggregate(Union('geom'))

        return assets['geom__union']
    
    def aggregate_points(self, qs):
        assets = qs.extra(where=["""
                                    geometrytype(geom) LIKE 'POINT'
                                 """])
        return assets
    
    def get_point_count_in_zone(self, zone, points):
        return zone.boundary.intersection(
            points.aggregate(Union('geom'))['geom__union']
        ).num_coords
