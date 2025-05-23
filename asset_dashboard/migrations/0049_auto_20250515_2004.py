# Generated by Django 3.2.19 on 2025-05-15 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0048_alter_phase_phase_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='requester',
            field=models.CharField(blank=True, choices=[('public_individual', 'Public (Individual)'), ('public_organization', 'Public (Organization)'), ('internal_pd', 'Internal (Planning and Development)'), ('internal_rm', 'Internal (Resource Management)'), ('internal_lm', 'Internal (Landscape Maintenance)'), ('internal_cep', 'Internal (Conservation and Experiential Programming)'), ('internal_police', 'Internal (Police)'), ('other', 'Internal (Other)'), ('elected_official', 'Elected Official')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('complete', 'Complete'), ('active', 'Active/In Progress'), ('inactive', 'Inactive/On Hold'), ('canceled', 'Canceled')], max_length=30, null=True),
        ),
    ]
