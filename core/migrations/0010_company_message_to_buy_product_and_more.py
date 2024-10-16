# Generated by Django 5.1.1 on 2024-10-11 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_company_landing_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='message_to_buy_product',
            field=models.TextField(default='Hola! me gustaría comprar este producto:', help_text="The message will be the one, that the user will send to the company to buy the product. e.g: 'I want to buy the product:'"),
        ),
        migrations.AlterField(
            model_name='company',
            name='whatsapp_number',
            field=models.CharField(blank=True, help_text='The number of the company in whatsapp. Dont use the +, write the extension number all together: 5491155555555', max_length=20, null=True),
        ),
    ]