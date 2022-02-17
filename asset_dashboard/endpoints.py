from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from asset_dashboard.models import Phase, Portfolio, PortfolioPhase, Project, \
    LocalAsset, Buildings, Signage, TrailsInfo, PoiInfo, PicnicGroves
from asset_dashboard.serializers import PortfolioSerializer, UserSerializer, \
    PortfolioPhaseSerializer, PhaseSerializer, ProjectSerializer, \
    BuildingsSerializer, TrailsSerializer, LocalAssetWriteSerializer, LocalAssetReadSerializer, \
    PointsOfInterestSerializer, PicnicGrovesSerializer, ParkingLotsSerializer, SignageSerializer


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class PortfolioPhaseViewSet(viewsets.ModelViewSet):
    queryset = PortfolioPhase.objects.all()
    serializer_class = PortfolioPhaseSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class PhaseViewSet(viewsets.ModelViewSet):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Buildings.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @property
    def asset_type(self):
        return self.request.query_params.get('asset_type', 'buildings')

    @property
    def model_cls(self):
        return {
            'buildings': {'model': Buildings},
            'trails': {'model': TrailsInfo},
            'points_of_interest': {'model': PoiInfo},
            'picnic_groves': {'model': PicnicGroves},
            'parking_lots': {'model': PoiInfo, 'check_for_not_null': True}
        }.get(self.asset_type, Buildings)

    @property
    def serializer_cls(self):
        return {
            'buildings': BuildingsSerializer,
            'trails': TrailsSerializer,
            'points_of_interest': PointsOfInterestSerializer,
            'picnic_groves': PicnicGrovesSerializer,
            'parking_lots': ParkingLotsSerializer
        }.get(self.asset_type, BuildingsSerializer)

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_cls

    def get_queryset(self, *args, **kwargs):
        search_filter = Q()

        if query := self.request.query_params.get('q', False):
            for field, field_type in self.model_cls.get('model').Search.fields:
                try:
                    field_type(query)
                except (ValueError, TypeError):
                    continue
                else:
                    search_filter |= Q(**{f'{field}__icontains': query})

            if self.model_cls.get('check_for_not_null'):
                for field in self.model_cls.get('model').Search.not_null_fields:
                    search_filter &= Q(**{f'{field}__isnull': False})

        return self.model_cls.get('model').objects.filter(search_filter)


class LocalAssetViewSet(viewsets.ModelViewSet):
    queryset = LocalAsset.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        """
        Get the appropriate serializer class depending on request type.
        See https://testdriven.io/blog/drf-serializers/#different-read-and-write-serializers
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return LocalAssetWriteSerializer
        return LocalAssetReadSerializer
