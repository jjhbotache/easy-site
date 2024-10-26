# Generated by Django 5.1.2 on 2024-10-26 16:13

import core.models
import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_company_enable_appointments'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='cancel_token',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='appointment_duration',
            field=models.FloatField(default=0.25, help_text='Duration must be 0.25, 0.5, or 1 hour.', validators=[django.core.validators.RegexValidator(message='Duration must be 0.25, 0.5, or 1 hour.', regex='^(0\\.25|0\\.5|1)$')]),
        ),
        migrations.AlterField(
            model_name='company',
            name='off_days_of_the_week',
            field=models.JSONField(default=core.models.default_off_days_of_the_week, help_text='List of off days of the week (e.g., [6, 7] for Sunday and Saturday)'),
        ),
        migrations.AlterField(
            model_name='company',
            name='off_hours',
            field=models.JSONField(default=core.models.default_off_hours, help_text='List of off hours (e.g., [12, 13, 14] for 12 PM, 1 PM, and 2 PM)'),
        ),
    ]
