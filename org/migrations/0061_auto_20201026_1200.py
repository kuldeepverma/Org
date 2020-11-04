# Generated by Django 3.0.9 on 2020-10-26 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0060_auto_20201022_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='personal_email_address',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employeeskillmapping',
            name='interested',
            field=models.BooleanField(default=False),
        ),
    ]
