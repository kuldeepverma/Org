# Generated by Django 3.0.9 on 2020-08-10 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0028_auto_20200804_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='primary_function',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='org.Function'),
            preserve_default=False,
        ),
    ]
