"""example_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

from asset_dashboard.endpoints import PortfolioViewSet, UserViewSet, \
    PortfolioPhaseViewSet, PhaseViewSet, ProjectViewSet, AssetViewSet
from asset_dashboard.views import ProjectListView, CipPlannerView, ProjectCreateView, \
                                    ProjectUpdateView, ProjectListJson, \
                                    ProjectsByDistrictListView, ProjectsByDistrictListJson


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'portfolios', PortfolioViewSet)
router.register(r'users', UserViewSet)
router.register(r'portfolio-phases', PortfolioPhaseViewSet)
router.register(r'phases', PhaseViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'assets', AssetViewSet)

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    path('projects/json/', ProjectListJson.as_view(), name='project-list-json'),
    path('projects/add-project/', ProjectCreateView.as_view(), name='add-project'),
    path('projects/<int:pk>/', ProjectUpdateView.as_view(), name='project-detail'),
    path('projects/districts/', ProjectsByDistrictListView.as_view(), name='projects-by-district'),
    path('projects/districts/json/', ProjectsByDistrictListJson.as_view(), name='projects-district-json'),
    path('cip-planner/', CipPlannerView.as_view(), name='cip-planner'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]

handler404 = 'asset_dashboard.views.page_not_found'
handler500 = 'asset_dashboard.views.server_error'
