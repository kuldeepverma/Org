# Generated by Django 3.0.8 on 2020-07-11 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0008_auto_20200711_2002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeedetail',
            old_name='primary_manager',
            new_name='primary_manager_id',
        ),
    ]
