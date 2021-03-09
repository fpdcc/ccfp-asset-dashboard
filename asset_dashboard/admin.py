from django.contrib import admin
from . import models


class ProjectCategoryAdmin(admin.ModelAdmin):
    exclude = ('name',)


class ProjectAdmin(admin.ModelAdmin):
    exclude = (
        'accessibility',
        'leverage_resource',
        'obligation',
        'phase_completion',
        'plan',
    )


admin.site.register(models.CommissionerDistrict)
admin.site.register(models.HouseDistrict)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.ProjectCategory, ProjectCategoryAdmin)
admin.site.register(models.ProjectFinances)
admin.site.register(models.ProjectScore)
admin.site.register(models.ScoreWeights)
admin.site.register(models.Section)
admin.site.register(models.SenateDistrict)
admin.site.register(models.Staff)
admin.site.register(models.Zone)
