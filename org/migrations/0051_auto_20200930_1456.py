# Generated by Django 3.0.9 on 2020-09-30 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0050_auto_20200906_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
