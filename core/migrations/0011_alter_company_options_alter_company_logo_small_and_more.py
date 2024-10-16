# Generated by Django 5.1.1 on 2024-10-15 23:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_company_message_to_buy_product_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Company'},
        ),
        migrations.AlterField(
            model_name='company',
            name='logo_small',
            field=models.ImageField(help_text='The logo of the company (small size and dark)', upload_to='logos/small/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]),
        ),
        migrations.AlterField(
            model_name='company',
            name='message_to_buy_product',
            field=models.CharField(default='Hola! me gustaría comprar este producto:', help_text="The message will be the one, that the user will send to the company to buy the product. e.g: 'I want to buy the product:'", max_length=255),
        ),
    ]