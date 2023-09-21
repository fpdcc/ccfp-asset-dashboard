# Generated by Django 3.2.19 on 2023-08-31 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0046_alter_phase_funding_streams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phasezonedistribution',
            name='phase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phase_zone_distribution', to='asset_dashboard.phase'),
        ),
        migrations.AlterField(
            model_name='phasezonedistribution',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phase_zone_distribution', to='asset_dashboard.zone'),
        ),
    ]
