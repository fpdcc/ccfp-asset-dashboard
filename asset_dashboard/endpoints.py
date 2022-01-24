from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from asset_dashboard.models import Phase, Portfolio, PortfolioPhase, Project, \
    LocalAsset, Buildings, TrailsInfo
from asset_dashboard.serializers import PortfolioSerializer, UserSerializer, \
    PortfolioPhaseSerializer, PhaseSerializer, ProjectSerializer, \
    LocalAssetSerializer, BuildingsSerializer, TrailsSerializer


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PortfolioPhaseViewSet(viewsets.ModelViewSet):
    queryset = PortfolioPhase.objects.all()
    serializer_class = PortfolioPhaseSerializer


class PhaseViewSet(viewsets.ModelViewSet):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Buildings.objects.all()

    @property
    def asset_type(self):
        return self.request.query_params.get('asset_type', 'buildings')

    @property
    def model_cls(self):
        return {
            'buildings': Buildings,
            'trails': TrailsInfo,
        }.get(self.asset_type, Buildings)

    @property
    def serializer_cls(self):
        return {
            'buildings': BuildingsSerializer,
            'trails': TrailsSerializer,
        }.get(self.asset_type, BuildingsSerializer)

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_cls

    def get_queryset(self, *args, **kwargs):
        search_filter = Q()

        if query := self.request.query_params.get('q', False):

            for field, field_type in self.model_cls.Search.fields:
                try:
                    field_type(query)
                except (ValueError, TypeError):
                    continue
                else:
                    search_filter |= Q(**{f'{field}__icontains': query})

        return self.model_cls.objects.filter(search_filter)


class LocalAssetViewSet(viewsets.ModelViewSet):
    queryset = LocalAsset.objects.all()
    serializer_class = LocalAssetSerializer
    
    def create(self, request, *args, **kwargs):
        # Overriding https://github.com/encode/django-rest-framework/blob/02eeb6fa003b5cbe3851ac18392f129d31a1a6bd/rest_framework/mixins.py#L16
        # The request body should send the data as a
        # GeoJSON FeatureCollection, but we need to save each
        # feature separately. So, instantiate the serializer
        # for each feature and save the data.
        
        # geojson_features = request.data['geojson']['features']
        # geojson_features = request.data
        print(request.data['features'])
        
        if isinstance(request.data['features'], list):
            serializer = self.get_serializer(data=request.data['features'], many=True)
        else:
            serializer = self.get_serializer(data=request.data['features'])

        print('serializer')
        print(serializer)
        serializer.is_valid(raise_exception=True)
        print('is valid')
        self.perform_create(serializer)
        print('perform create')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                    headers=headers)
        # headers = {}
        # for feature in request.data['geojson']['features']:
        #     serializer = self.get_serializer(data={'geom': feature})
        #     serializer.is_valid(raise_exception=True)
        #     self.perform_create(serializer)
        #     headers.update({
        #         **self.get_success_headers(serializer.data)
        #     })
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    
    # def perform_create(self, serializer):
    #     phase_id = 2 
    #     print('perform create')
    #     print('serializer')
    #     print(serializer.initial_data)
    #     for feature in serializer.initial_data['geojson']['features']:
    #         serializer.save(feature)
        
    # def list(self):
    #     # hardcoding phase_id for now
    #     # will address with issue #94
    #     phase_id = 2
    #     return LocalAsset.objects.filter(phase__id=phase_id)
