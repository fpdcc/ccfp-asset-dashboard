from django.contrib import admin
from . import models


class ProjectCategoryAdmin(admin.ModelAdmin):
    exclude = ('name',)


admin.site.register(models.CommissionerDistrict)
admin.site.register(models.HouseDistrict)
admin.site.register(models.Project)
admin.site.register(models.ProjectCategory, ProjectCategoryAdmin)
admin.site.register(models.FundingStream)
admin.site.register(models.ProjectScore)
admin.site.register(models.ScoreWeights)
admin.site.register(models.Section)
admin.site.register(models.SenateDistrict)
admin.site.register(models.Staff)
admin.site.register(models.Zone)
