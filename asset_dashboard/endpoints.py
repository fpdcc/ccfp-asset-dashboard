from django.contrib.auth.models import User
from rest_framework import viewsets

from asset_dashboard.models import Phase, Portfolio, PortfolioPhase, Project
from asset_dashboard.serializers import PortfolioSerializer, UserSerializer, \
    PortfolioPhaseSerializer, PhaseSerializer, ProjectSerializer


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
