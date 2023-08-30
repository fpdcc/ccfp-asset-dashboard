# Generated by Django 3.2.19 on 2023-07-12 19:32

import asset_dashboard.models
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0041_project_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectscore',
            name='core_mission_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='ease_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='geographic_distance_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='operations_impact_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='social_equity_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='sustainability_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]