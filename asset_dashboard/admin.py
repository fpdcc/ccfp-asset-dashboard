from django.contrib import admin
from . import models


admin.site.register(models.Project)
admin.site.register(models.ProjectCategory)
admin.site.register(models.ScoreWeights)
admin.site.register(models.Section)
admin.site.register(models.Staff)
