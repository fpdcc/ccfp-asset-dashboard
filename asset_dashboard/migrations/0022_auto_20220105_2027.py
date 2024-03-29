# Generated by Django 3.1.7 on 2022-01-05 20:27

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0021_add_portfolio'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=3435)),
                ('building_id', models.BigIntegerField()),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_dashboard.phase')),
            ],
        ),
        migrations.DeleteModel(
            name='Asset',
        ),
    ]
