import uuid
from pytz import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, EmailValidator, RegexValidator
from django.db import models
from django.forms import  ValidationError
from django.utils.timezone import make_aware, is_aware, now
from cloudinary.models import CloudinaryField
from django.conf import settings

class User(AbstractUser):
    is_company_admin = models.BooleanField(default=True, help_text="Indica si el usuario es un administrador de la empresa.")
    is_staff = models.BooleanField(default=True, help_text="Indica si el usuario puede acceder al sitio de administración.")
  


def default_off_hours():return [12, 13, 14]
def default_off_days_of_the_week(): return [6,7]
class Company(models.Model):
    name = models.CharField(max_length=255, help_text=f"Nombre de la empresa. puedes acceder a tu web accediendo a ' {settings.FRONT_URL}/nombre de la empresa '.")
    company_description = models.TextField(blank=True, null=True, help_text="Descripción detallada de la empresa. Esta aparecerá en las páginas de 'inicio' y 'nosotros'.")
    # colores   
    background_color = models.CharField(max_length=7, default="ffffff,", help_text="Color de fondo en formato hexadecimal. Suele ser cercano a blanco (por ejemplo, #FFFFFF).")
    text_color = models.CharField(max_length=7, default="000000", help_text="Color del texto en formato hexadecimal. Suele ser cercano a negro (por ejemplo, #000000).")
    primary_color = models.CharField(max_length=7, default="967AA1", help_text="Color primario en formato hexadecimal (tono más oscuro).")
    secondary_color = models.CharField(max_length=7, default="AAA1C8", help_text="Color secundario en formato hexadecimal. Suele ser un color armónico al primario (tono más claro).")
    # medios
    logo_small = CloudinaryField('image', help_text="Logo de la empresa (tamaño pequeño, versión oscura). Se usará en la navbar y en el icono de la web.")
    logo_large = CloudinaryField('image', help_text="Logo de la empresa (tamaño grande) Se usará de fondo en la página 'nosotros'.")
    # datos de la empresa
    country_utc_offset = models.IntegerField(default=-5, help_text="Desplazamiento UTC del país de la empresa (por ejemplo, -5 para Colombia). Se usa para el calendario de las citas")
    location = models.CharField(max_length=255, help_text="Dirección física o ubicación de la empresa. Aparecerá en el fotter de la página")
    email = models.EmailField(help_text="Correo electrónico de contacto de la empresa. Aparecerá en el fotter de la página")
    instagram = models.URLField(blank=True, null=True, help_text="URL del perfil de Instagram de la empresa. Aparecerá en el fotter de la página")
    facebook = models.URLField(blank=True, null=True, help_text="URL de la página de Facebook de la empresa. Aparecerá en el fotter de la página")
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Número de WhatsApp sin '+', incluir código de país y número juntos (por ejemplo, +54 91155555555 -> 5491155555555)."
    )
    whatsapp_message = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Mensaje predeterminado enviado por los usuarios al contactar vía el botón de WhatsApp. Si no agregas un mensaje, No aparecerá el botón de WhatsApp."
    )
    # más datos
    message_to_buy_product = models.CharField(
        max_length=255,
        default="Hola! me gustaría comprar este producto:",
        help_text="Mensaje predeterminado que los usuarios envían para expresar interés en comprar un producto."
    )
    product_description = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción general de los productos de la empresa. Esta descripción estará en la página de 'nosotros'."
    )
    general_data_for_products = models.TextField(
        blank=True,
        null=True,
        help_text="Información adicional mostrada en cada página de producto. Esta descripción estará justo abajo de cada producto en la página de cada producto."
    )
    
    # Configuración del calendario
    enable_appointments = models.BooleanField(
        default=True,
        help_text="Habilitar o deshabilitar la función de programación de citas."
    )
    appointment_duration = models.FloatField(
        default=0.25, 
        help_text="Duración de cada cita en horas (debe ser 0.25, 0.5 o 1).",
        validators=[RegexValidator(regex=r'^(0\.25|0\.5|1)$', message="La duración debe ser 0.25, 0.5 o 1 hora.")]
    )
    appointment_start_time = models.IntegerField(
        default=8,
        help_text="Hora de inicio para citas (por ejemplo, 8 para las 8 AM)."
    )
    appointment_end_time = models.IntegerField(
        default=20,
        help_text="Hora de finalización para citas (por ejemplo, 20 para las 8 PM)."
    )
    off_hours = models.JSONField(
        default=default_off_hours,
        help_text="Lista de horas cuando no se pueden programar citas (por ejemplo, [12, 13, 14] para de 12 PM a 2 PM)."
    )
    off_days_of_the_week = models.JSONField(
        default=default_off_days_of_the_week,
        help_text="Lista de días cuando no hay disponibilidad para citas (por ejemplo, [6, 7] para sábado y domingo)."
    )

    owner = models.OneToOneField(
        'core.User',
        on_delete=models.CASCADE,
        related_name='company',
        help_text="El usuario propietario de esta empresa."
    )
    
    class Meta:
        verbose_name_plural = "Company"

    def __str__(self):
        return self.name



class Product(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='products',
        help_text="La empresa que ofrece este producto."
    )
    name = models.CharField(max_length=255, help_text="Nombre del producto.")
    description = models.TextField(help_text="Descripción detallada del producto.")
    features = models.TextField( help_text="Características del producto, separadas por comas.")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio del producto en moneda local."
    )
    image = CloudinaryField(
        'image',
        help_text="Imagen del producto (orientación horizontal con la parte principal a la derecha)."
    )

    def __str__(self):
        return f"{self.name} - {self.company}"
    
class Appointment(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='appointments',
        help_text="La empresa con la que se agenda la cita."
    )
    start_datetime = models.DateTimeField(help_text="Fecha y hora de inicio de la cita.")
    end_datetime = models.DateTimeField(help_text="Fecha y hora de finalización de la cita.")
    full_name = models.CharField(max_length=255, help_text="Nombre completo de la persona que agenda la cita.")
    email = models.EmailField(
        blank=True,
        null=True,
        validators=[EmailValidator()],
        help_text="Correo electrónico de la persona que agenda la cita."
    )
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        validators=[
            RegexValidator(
                regex=r'^\d{10,15}$',
                message="Ingrese un número de teléfono válido."
            )
        ],
        help_text="Número de teléfono de contacto de la persona que agenda la cita."
    )
    message = models.TextField(
        blank=True,
        null=True,
        help_text="Mensaje adicional o notas para la cita."
    )
    cancel_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        help_text="Token único utilizado para cancelar la cita."
    )
    
    def __str__(self):
        local_tz = timezone(f'Etc/GMT+{abs(self.company.country_utc_offset)}')
        start_datetime_local = self.start_datetime.astimezone(local_tz)
        end_datetime_local = self.end_datetime.astimezone(local_tz)
        return f"{self.company}) {self.full_name} {start_datetime_local.strftime('%d/%m/%Y %H:%M')} - {end_datetime_local.strftime('%H:%M %d/%m/%Y ')} ({local_tz})"
    
    def clean(self):
        # Validar que la cita no esté en un día de descanso
        day_of_week = self.start_datetime.weekday() + 1  # Monday is 0 in Python, so add 1 to match the model's convention
        if day_of_week in self.company.off_days_of_the_week:
            print(f"No se pueden agendar citas los días {day_of_week}.")
            raise ValidationError(f"No se pueden agendar citas los días {day_of_week}.")

        # Validar que la cita no esté en una hora de descanso
        start_hour = self.start_datetime.hour + (self.company.country_utc_offset)
        end_hour = self.end_datetime.hour + (self.company.country_utc_offset)
        if start_hour in self.company.off_hours or end_hour in self.company.off_hours:
            print(f"No se pueden agendar citas en las horas de descanso: {start_hour} - {end_hour} - {self.company.off_hours}")
            print(f"Start hour: {self.start_datetime} - End hour: {self.end_datetime}")
            raise ValidationError("No se pueden agendar citas en las horas de descanso.")
        
        # Convert all datetimes to aware and ensure they are aware
        if not is_aware(self.start_datetime):self.start_datetime = make_aware(self.start_datetime)
        if not is_aware(self.end_datetime):self.end_datetime = make_aware(self.end_datetime)
        
        # Validar que la cita no esté en el pasado    
        current_time = now()
        
        # print(f"Current time: {current_time}")
        # print(f"Appointment start time: {self.start_datetime}")
        
        if self.start_datetime < current_time:
            raise ValidationError("No se pueden agendar citas en el pasado.")

        # Validar que la cita termine después de que empieza
        if self.end_datetime <= self.start_datetime:
            raise ValidationError("La cita debe terminar después de que empieza.")

        # Validar que la duración de la cita sea correcta
        duration = (self.end_datetime - self.start_datetime).total_seconds() / 3600.0 + 1/60.0 # add 1 minute to the duration
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
