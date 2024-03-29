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
    PortfolioPhaseViewSet, PhaseViewSet, ProjectViewSet, AssetViewSet, LocalAssetViewSet, \
    PromotePhaseView, CountywideView, FundingStreamView
from asset_dashboard.views import ProjectListView, CipPlannerView, ProjectCreateView, \
                                    ProjectUpdateView, ProjectListJson, ProjectDeleteView, \
                                    ProjectsByDistrictListView, ProjectsByDistrictListJson, \
                                    PhaseCreateView, PhaseUpdateView, \
                                    AssetAddEditView, PhaseDeleteView, FundingStreamDeleteView, pong\


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'portfolios', PortfolioViewSet)
router.register(r'users', UserViewSet)
router.register(r'portfolio-phases', PortfolioPhaseViewSet)
router.register(r'phases', PhaseViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'local-assets', LocalAssetViewSet)

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    path('projects/json/', ProjectListJson.as_view(), name='project-list-json'),
    path('projects/add-project/', ProjectCreateView.as_view(), name='add-project'),
    path('projects/<int:pk>/', ProjectUpdateView.as_view(), name='project-detail'),
    path('projects/delete/<int:pk>/', ProjectDeleteView.as_view(), name='delete-project'),
    path('projects/<int:pk>/phases/create/', PhaseCreateView.as_view(), name='create-phase'),
    path('projects/phases/edit/<int:pk>/', PhaseUpdateView.as_view(), name='edit-phase'),
    path('projects/phases/delete/<int:pk>/', PhaseDeleteView.as_view(), name='delete-phase'),
    path('projects/phases/<int:pk>/funding/delete/', FundingStreamDeleteView.as_view(), name='delete-funding'),
    path('projects/phases/edit/<int:pk>/assets/', AssetAddEditView.as_view(), name='create-update-assets'),
    path('projects/phases/promote/assets/', PromotePhaseView.as_view(), name='promote-assets-phase'),
    path('projects/phases/assets/countywide/', CountywideView.as_view(), name='countywide'),
    path('projects/phases/fundingstream/', FundingStreamView.as_view(), name='create-update-funding'),
    path('projects/districts/', ProjectsByDistrictListView.as_view(), name='projects-by-district'),
    path('projects/districts/json/', ProjectsByDistrictListJson.as_view(), name='projects-district-json'),
    path('cip-planner/', CipPlannerView.as_view(), name='cip-planner'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('pong/', pong),
]

handler404 = 'asset_dashboard.views.page_not_found'
handler500 = 'asset_dashboard.views.server_error'
