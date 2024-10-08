# Generated by Django 5.1.1 on 2024-10-06 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_company_company_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='background_color',
            field=models.CharField(default=222, max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='primary_color',
            field=models.CharField(default=222, max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='secondary_color',
            field=models.CharField(default=222, max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='text_color',
            field=models.CharField(default=222, max_length=7),
            preserve_default=False,
        ),
    ]