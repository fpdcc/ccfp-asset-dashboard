# Generated by Django 3.1.7 on 2022-03-28 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0031_auto_20220328_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_manager',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]