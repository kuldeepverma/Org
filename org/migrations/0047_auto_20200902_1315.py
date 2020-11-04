# Generated by Django 3.0.9 on 2020-09-02 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0046_userrolemapping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrolemapping',
            name='user',
        ),
        migrations.AddField(
            model_name='userrolemapping',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='org.Employee'),
            preserve_default=False,
        ),
    ]
