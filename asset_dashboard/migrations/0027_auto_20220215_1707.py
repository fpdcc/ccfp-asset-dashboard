# Generated by Django 3.1.7 on 2022-02-15 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0026_auto_20220207_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localasset',
            name='asset_id',
            field=models.CharField(blank=True, max_length=1000000, null=True),
        ),
    ]
