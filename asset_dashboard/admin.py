from django.contrib import admin
from .models import Project, ProjectCategory, Section, Plan, Staff, ProjectScore

admin.site.register(Project)
admin.site.register(ProjectCategory)
admin.site.register(Section)
admin.site.register(Plan)
admin.site.register(Staff)
admin.site.register(ProjectScore)
