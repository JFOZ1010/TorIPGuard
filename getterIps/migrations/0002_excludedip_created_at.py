# Generated by Django 4.0.4 on 2024-08-22 12:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('getterIps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='excludedip',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
