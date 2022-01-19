from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, \
    GeometryField, GeometrySerializerMethodField

from asset_dashboard.models import Phase, Portfolio, PortfolioPhase, Project, \
    Buildings, TrailsInfo, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'category', 'section_owner',)


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ('id',)


class PortfolioPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioPhase
        fields = ('phase', 'sequence',)


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'user', 'created_at', 'updated_at', 'phases',)

    phases = PortfolioPhaseSerializer(many=True, read_only=False)

    def create(self, validated_data):
        phase_data = validated_data.pop('phases')

        portfolio = Portfolio.objects.create(**validated_data)

        for phase in phase_data:
            PortfolioPhase.objects.create(
                portfolio=portfolio,
                phase=phase['phase'],
                sequence=phase['sequence']
            )

        return portfolio

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        phase_data = validated_data.get('phases', [])

        if phase_data:
            for_create = []
            for_update = []

            # TODO: This could be made more efficient by getting all existing
            # PortfolioPhase instances in a single query, updating the sequence
            # from phase data, then performing a bulk update. Will revisit if
            # performance is a concern.
            for phase in phase_data:
                try:
                    portfolio_phase = PortfolioPhase.objects.get(
                        portfolio=instance,
                        phase=phase['phase']
                    )
                except PortfolioPhase.DoesNotExist:
                    portfolio_phase = PortfolioPhase(
                        portfolio=instance,
                        phase=phase['phase'],
                        sequence=phase['sequence']
                    )
                    for_create.append(portfolio_phase)
                else:
                    portfolio_phase.sequence = phase['sequence']
                    for_update.append(portfolio_phase)

            PortfolioPhase.objects.bulk_create(for_create)
            PortfolioPhase.objects.bulk_update(for_update, ['sequence'])

            PortfolioPhase.objects.filter(portfolio=instance)\
                                  .exclude(phase__in=tuple(phase['phase'] for phase in phase_data))\
                                  .delete()

        return instance


class NullableIntegerField(serializers.IntegerField):

    def __init__(self, *args, allow_null=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_null = allow_null

    def to_representation(self, value):
        if self.allow_null and value is None:
            return None
        return super().to_representation(value)


class BuildingsSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Buildings
        fields = ('identifier', 'name', 'geom')
        geo_field = 'geom'

    identifier = NullableIntegerField(source='fpd_uid', allow_null=True)
    name = serializers.CharField(source='building_name')
    geom = GeometrySerializerMethodField()
    
    def get_geom(self, obj):
        return obj.geom.transform(4326, clone=True)


class TrailsSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrailsInfo
        fields = ('identifier', 'name', 'geom')
        geo_field = 'geom'

    identifier = serializers.IntegerField(source='trails_id')
    name = serializers.CharField(source='trail_subsystem')
    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        '''
        This is heavy, might want to consider pre-fetching related Trails obj
        in viewset -> get_queryset
        '''
        return obj.trails.geom.transform(4326, clone=True)
