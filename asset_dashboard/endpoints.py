<<<<<<< HEAD
from rest_framework import viewsets

from asset_dashboard.models import Portfolio
from asset_dashboard.serializers import PortfolioSerializer
=======
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import viewsets

from asset_dashboard.models import Phase, Portfolio, PortfolioPhase, Project, \
    Buildings, TrailsInfo
from asset_dashboard.serializers import PortfolioSerializer, UserSerializer, \
    PortfolioPhaseSerializer, PhaseSerializer, ProjectSerializer, \
    BuildingsSerializer, TrailsSerializer

import asset_dashboard.models as ad_models
import asset_dashboard.serializers as ad_serializers
>>>>>>> Spike asset API with DRF


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
<<<<<<< HEAD
=======


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
                except ValueError:
                    continue
                else:
                    search_filter |= Q(**{f'{field}__icontains': query})

        return self.model_cls.objects.filter(search_filter)
>>>>>>> Spike asset API with DRF
