# Generated by Django 3.0.9 on 2020-10-19 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0055_skill_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmapping',
            name='skill',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='org.EmployeeSkillMapping'),
        ),
        migrations.DeleteModel(
            name='ProjectSkillMapping',
        ),
    ]
