from django.contrib import admin
from .models import CommissionerDistrict, HouseDistrict, Plan, Project, ProjectCategory, ProjectScore, Section, SenateDistrict, Staff, Zone


class ProjectCategoryAdmin(admin.ModelAdmin):
    exclude = ('name',)


admin.site.register(CommissionerDistrict)
admin.site.register(HouseDistrict)
admin.site.register(Plan)
admin.site.register(Project)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(ProjectScore)
admin.site.register(Section)
admin.site.register(SenateDistrict)
admin.site.register(Staff)
admin.site.register(Zone)
