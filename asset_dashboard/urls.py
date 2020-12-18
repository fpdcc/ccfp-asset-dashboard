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

from asset_dashboard.views import ProjectListView, Home, AddEditProjectFormView, ProjectDetailView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('projects/add-edit-project/', AddEditProjectFormView.as_view(), name='add-edit-projects'),
    path('projects/<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('admin/', admin.site.urls),
]

handler404 = 'asset_dashboard.views.page_not_found'
handler500 = 'asset_dashboard.views.server_error'
