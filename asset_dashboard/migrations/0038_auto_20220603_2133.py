# Generated by Django 3.1.7 on 2022-06-03 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_dashboard', '0037_auto_20220513_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='projectcategory',
            name='subcategory',
        ),
        migrations.AlterField(
            model_name='projectcategory',
            name='name',
            field=models.TextField(),
        ),
    ]
