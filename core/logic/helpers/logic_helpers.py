import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import dotenv
import os

from core.logic.helpers.str_helpers import get_company_name_from_url
from core.models import Company

# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv()

# Obtener la contraseña de la aplicación de Google desde las variables de entorno
SENDER = "pyautoemail000@gmail.com"
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")

def send_gmail(recipient_email, subject, body):
    try:
        # Configuración del servidor SMTP de Gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Crear el objeto del mensaje
        msg = MIMEMultipart()
        msg['From'] = SENDER
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Conectar al servidor SMTP y enviar el correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(SENDER, GOOGLE_APP_PASSWORD)
            server.send_message(msg)

        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def company_from_request(request):
    company_text = get_company_name_from_url(request.get_full_path())
    company = Company.objects.filter(name__icontains=company_text).order_by('name')[0]
    return company