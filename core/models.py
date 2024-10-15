from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator
from django.db import models

class User(AbstractUser):
  is_company_admin = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=True)
  
  def save(self, *args, **kwargs):
      print(self.password, end=' -> ')
      self.password = make_password(self.password)
      super().save(*args, **kwargs)

class Company(models.Model):
    name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    # colors
    background_color = models.CharField(max_length=7,help_text="The color in hexadesimal")
    text_color = models.CharField(max_length=7,help_text="The color in hexadesimal")
    primary_color = models.CharField(max_length=7,help_text="The color in hexadesimal (darker)")
    secondary_color = models.CharField(max_length=7,help_text="The color in hexadesimal (lighter)")
    # media
    logo_small = models.ImageField(upload_to='logos/small/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])], help_text="The logo of the company (small size and dark)")
    logo_large = models.ImageField(upload_to='logos/large/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])
    # company data
    location = models.CharField(max_length=255)
    email = models.EmailField()
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True, help_text="The number of the company in whatsapp. Dont use the +, write the extension number all together: 5491155555555")
    whatsapp_message = models.CharField(max_length=255, blank=True, null=True, help_text="The message that will be sent by the user to the company")
    # more data
    general_data_for_products = models.TextField(blank=True, null=True, help_text="General data that will be shown in each product of page")
    message_to_buy_product = models.TextField(default="Hola! me gustaría comprar este producto:", help_text="The message will be the one, that the user will send to the company to buy the product. e.g: 'I want to buy the product:'")
    
    owner = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return self.name

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    features = models.TextField( help_text="The features of the product. Separate each feature with a comma.")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', help_text="The image of the product (horizontal orientation with main part at the right))", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])

    def __str__(self):
        return self.name
    
