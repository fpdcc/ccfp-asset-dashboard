# Generated by Django 3.1.6 on 2021-02-05 21:14

import asset_dashboard.models
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0009_auto_20210205_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectscore',
            name='core_mission_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='ease_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='geographic_distance_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='operations_impact_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='social_equity_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='projectscore',
            name='sustainability_score',
            field=asset_dashboard.models.ScoreField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
