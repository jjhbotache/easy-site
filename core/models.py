import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator, EmailValidator, RegexValidator
from django.db import models
from django.forms import DateTimeField, ValidationError
from django.utils.timezone import make_aware, is_aware

class User(AbstractUser):
  is_company_admin = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=True)
  
  def save(self, *args, **kwargs):
      print(self.password, end=' -> ')
      self.password = make_password(self.password)
      super().save(*args, **kwargs)


def default_off_hours():return [12, 13, 14]
def default_off_days_of_the_week(): return [6,7]
class Company(models.Model):
    name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    # colors
    background_color = models.CharField(max_length=7, help_text="The color in hexadesimal")
    text_color = models.CharField(max_length=7, help_text="The color in hexadesimal")
    primary_color = models.CharField(max_length=7, help_text="The color in hexadesimal (darker)")
    secondary_color = models.CharField(max_length=7, help_text="The color in hexadesimal (lighter)")
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
    message_to_buy_product = models.CharField(max_length=255, default="Hola! me gustaría comprar este producto:", help_text="The message will be the one, that the user will send to the company to buy the product. e.g: 'I want to buy the product:'")
    general_data_for_products = models.TextField(blank=True, null=True, help_text="General data that will be shown in each product of page")
    
    # Calendar configuration
    enable_appointments = models.BooleanField(default=True, help_text="Enable or disable appointments (calendar)")
    appointment_duration = models.FloatField(
        default=0.25, 
        help_text="Duration must be 0.25, 0.5, or 1 hour.",
        validators=[RegexValidator(regex=r'^(0\.25|0\.5|1)$', message="Duration must be 0.25, 0.5, or 1 hour.")]
    )
    appointment_start_time = models.IntegerField(default=8, help_text="Start time for appointments (e.g., 8 for 8 AM)")
    appointment_end_time = models.IntegerField(default=20, help_text="End time for appointments (e.g., 20 for 8 PM)")
    off_hours = models.JSONField(default=default_off_hours, help_text="List of off hours (e.g., [12, 13, 14] for 12 PM, 1 PM, and 2 PM)")
    off_days_of_the_week = models.JSONField(default=default_off_days_of_the_week, help_text="List of off days of the week (e.g., [6, 7] for Sunday and Saturday)")

    owner = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='company')
    
    class Meta:
        verbose_name_plural = "Company"

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
        return f"{self.name} - {self.company}"
    
class Appointment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='appointments')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True, validators=[EmailValidator()])
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(regex=r'^\d{10,15}$', message="Enter a valid phone number.")]
    )
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.company}) {self.full_name} {self.start_datetime.strftime('%d/%m/%Y %H:%M')} - {self.end_datetime.strftime('%H:%M %d/%m/%Y ')}"
    
    def clean(self):
        # Validar que la cita no esté en un día de descanso
        day_of_week = self.start_datetime.weekday() + 1  # Monday is 0 in Python, so add 1 to match the model's convention
        if day_of_week in self.company.off_days_of_the_week:
            raise ValidationError(f"No se pueden agendar citas los días {day_of_week}.")

        # Validar que la cita no esté en una hora de descanso
        start_hour = self.start_datetime.hour
        end_hour = self.end_datetime.hour
        if start_hour in self.company.off_hours or end_hour in self.company.off_hours:
            raise ValidationError("No se pueden agendar citas en las horas de descanso.")
        
        # Convert all datetimes to aware and ensure they are aware
        if not is_aware(self.start_datetime):self.start_datetime = make_aware(self.start_datetime)
        if not is_aware(self.end_datetime):self.end_datetime = make_aware(self.end_datetime)
        
        # Validar que la cita no esté en el pasado    
        current_time = make_aware(datetime.datetime.now())
        
        if self.start_datetime < current_time:
            raise ValidationError("No se pueden agendar citas en el pasado.")

        # Validar que la cita termine después de que empieza
        if self.end_datetime <= self.start_datetime:
            raise ValidationError("La cita debe terminar después de que empieza.")

        # Validar que la duración de la cita sea correcta
        duration = (self.end_datetime - self.start_datetime).total_seconds() / 3600.0
        if duration % self.company.appointment_duration != 0:
            raise ValidationError(f"La duración de la cita debe ser de {self.company.appointment_duration} horas o un múltiplo de la misma.")


        # Validar que la cita no se superponga con otra cita existente
        overlapping_appointments = Appointment.objects.filter(
            company=self.company,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime
        ).exclude(id=self.id)
        if overlapping_appointments.exists():
            raise ValidationError("La cita se superpone con otra cita existente.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean() y valida el modelo antes de guardar
        super().save(*args, **kwargs)