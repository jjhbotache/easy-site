# Generated by Django 5.1.1 on 2024-10-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
