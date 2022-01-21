from django.contrib.auth.models import User
from rest_framework import viewsets

from asset_dashboard.models import Portfolio
from asset_dashboard.serializers import PortfolioSerializer


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
