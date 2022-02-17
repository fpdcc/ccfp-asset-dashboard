from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, \
    GeometrySerializerMethodField, GeometryField

from asset_dashboard.models import Phase, Portfolio, PortfolioPhase, Project, \
    LocalAsset, Buildings, TrailsInfo, PoiInfo, PointsOfInterest, PicnicGroves, \
    ParkingLots


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


class NullableCharField(serializers.CharField):
    def __init__(self, *args, allow_null=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_null = allow_null
    
    def to_representation(self, value):
        if self.allow_null and value is None:
            return None
        return super().to_representation(value)
    

class BaseLocalAssetSerializer(GeoFeatureModelSerializer):
    """
    A base serializer for the LocalAssets because we need
    different `geom` field types for read-only and write-only.
    See https://stackoverflow.com/a/67464485.
    """

    class Meta:
        model = LocalAsset
        fields = ('id', 'geom', 'asset_id', 'asset_type', 'asset_name', 'phase')
        geo_field = 'geom'

    asset_id = NullableCharField(allow_null=True)
    asset_type = serializers.CharField(source='asset_model')
    asset_name = serializers.CharField()
    phase = serializers.PrimaryKeyRelatedField(queryset=Phase.objects.all())

    def get_geom(self, obj):
        return obj.geom.transform(4326, clone=True)


class LocalAssetWriteSerializer(BaseLocalAssetSerializer):
    geom = GeometryField()


class LocalAssetReadSerializer(BaseLocalAssetSerializer):
    geom = GeometrySerializerMethodField()


class SourceAssetSerializer(GeoFeatureModelSerializer):
    class Meta:
        fields = ('source')

    source = serializers.SerializerMethodField()

    def get_source(self, obj):
        return 'search'

class BuildingsSerializer(SourceAssetSerializer):
    class Meta:
        model = Buildings
        fields = ('identifier', 'name', 'geom', 'source')
        geo_field = 'geom'

    identifier = NullableIntegerField(source='fpd_uid', allow_null=True)
    name = serializers.CharField(source='building_name')
    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        return obj.geom.transform(4326, clone=True)


class TrailsSerializer(SourceAssetSerializer):
    class Meta:
        model = TrailsInfo
        fields = ('identifier', 'name', 'geom', 'source')
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

class PointsOfInterestSerializer(SourceAssetSerializer):
    class Meta:
        model = PoiInfo
        fields = ('identifier', 'name', 'geom', 'source')
        geo_field = 'geom'
    
    identifier = serializers.IntegerField(source='fpd_uid')
    name = serializers.SerializerMethodField(source='nameid')
    geom = GeometrySerializerMethodField()
    
    def get_geom(self, obj):
        return PointsOfInterest.objects.get(
            id=obj.pointsofinterest_id
        ).geom.transform(4326, clone=True)
    
    def get_name(self, obj):
        return obj.nameid.name

class PicnicGrovesSerializer(SourceAssetSerializer):
    class Meta:
        model = PicnicGroves
        fields = ('identifier', 'name', 'geom', 'source')
        geo_field = 'geom'

    identifier = serializers.CharField(source='fpd_uid')
    name = serializers.SerializerMethodField(source='poi_info__nameid')
    geom = GeometrySerializerMethodField()
    
    def get_geom(self, obj):
        return obj.geom.transform(4326, clone=True)

    def get_name(self, obj):
        return obj.poi_info.nameid.name

class ParkingLotsSerializer(SourceAssetSerializer):
    class Meta:
        model = PoiInfo # Need to use PoiInfo.name and PoiInfo.fpd_uid to lookup ParkingLots
        fields = ('identifier', 'name', 'geom', 'source')
        geo_field = 'geom'

    identifier = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        return ParkingLots.objects.get(id=obj.parking_info.lot_id).geom.transform(4326, clone=True)

    def get_name(self, obj):
        return obj.nameid.name
    
    def get_identifier(self, obj):
        return  obj.fpd_uid
