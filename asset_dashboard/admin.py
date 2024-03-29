from django.contrib import admin
from . import models


admin.site.register(models.Project)
admin.site.register(models.ProjectCategory)
admin.site.register(models.ScoreWeights)
admin.site.register(models.Section)
admin.site.register(models.Staff)
admin.site.register(models.Phase)
admin.site.register(models.PhaseZoneDistribution)
admin.site.register(models.Zone)
admin.site.register(models.HouseDistrict)
admin.site.register(models.SenateDistrict)
admin.site.register(models.CommissionerDistrict)
