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
from django.urls import path

from asset_dashboard.views import ProjectListView, CipPlannerView, ProjectCreateView, ProjectUpdateView, ProjectListJson

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    path('projects/json', ProjectListJson.as_view(), name='project-list-json'),
    path('projects/add-project/', ProjectCreateView.as_view(), name='add-project'),
    path('projects/<int:pk>/', ProjectUpdateView.as_view(), name='project-detail'),
    path('cip-planner', CipPlannerView.as_view(), name='cip-planner'),
    path('admin/', admin.site.urls),
]

handler404 = 'asset_dashboard.views.page_not_found'
handler500 = 'asset_dashboard.views.server_error'
