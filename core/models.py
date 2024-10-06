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
    
    logo_small = models.ImageField(upload_to='logos/small/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])
    logo_large = models.ImageField(upload_to='logos/large/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])
    location = models.CharField(max_length=255)
    email = models.EmailField()
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    owner = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='company')
    landing_type = models.CharField(max_length=50, choices=[('carousel', 'Carousel'), ('video', 'Video')])
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_message = models.CharField(max_length=255, blank=True, null=True, help_text="The message that will be sent by the user to the company")

    def __str__(self):
        return self.name

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    
