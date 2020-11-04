# Generated by Django 3.0.8 on 2020-07-12 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0012_employee_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='function',
            name='function_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Employee'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_ba',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ba_employee', to='org.Employee'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pm_employee', to='org.Employee'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='po_employee', to='org.Employee'),
        ),
    ]
