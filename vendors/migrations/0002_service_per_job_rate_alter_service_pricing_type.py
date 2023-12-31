# Generated by Django 4.2.7 on 2023-12-14 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='per_job_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='pricing_type',
            field=models.CharField(choices=[('hourly', 'Hourly'), ('daily', 'Daily'), ('per_job', 'Job')], max_length=20),
        ),
    ]
