from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.db.models.fields import IntegerField
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, \
    GeometrySerializerMethodField
from rest_framework.exceptions import ErrorDetail, ValidationError

from asset_dashboard.models import LocalAsset, Phase, Portfolio, PortfolioPhase, Project, \
    LocalAsset, Buildings, TrailsInfo


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

    def update(self, validated_data):
        ...


class NullableIntegerField(serializers.IntegerField):

    def __init__(self, *args, allow_null=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_null = allow_null

    def to_representation(self, value):
        if self.allow_null and value is None:
            return None
        return super().to_representation(value)
    
class LocalAssetSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = LocalAsset
        geo_field = 'geometry'

    # id = serializers.IntegerField()
    geometry = GeometrySerializerMethodField(source='geom')
    # asset_id = serializers.IntegerField(source='')
    # phase = serializers.RelatedField(source='phase.id', read_only=True)

    def get_geom(self, obj):
        return obj.geom.transform(4326, clone=True)

    def create(self, validated_data):
        print('create')
        # geo = local_asset, _ = LocalAsset.objects.get_or_create(
        #         geom=GEOSGeometry(json.dumps(feature['geometry'])),
        #         # TODO implement type, (like building id etc)
        #         building_id=feature['properties']['pk'], 
        #         phase_id=phase
        #     )
        print('validated data')
        from pprint import pprint
        pprint(self.__dict__)
        print(validated_data)
        return LocalAsset.objects.create(**validated_data)

    def validate_geom(self):
        print('validate geom')
        
    def is_valid(self, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )
        
        print('is valid')

        if not hasattr(self, '_validated_data'):
            print('if not has attribute')
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)


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
