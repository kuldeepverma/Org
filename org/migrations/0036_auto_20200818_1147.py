# Generated by Django 3.0.9 on 2020-08-18 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0035_projectmapping_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrole',
            name='role',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
