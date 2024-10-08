import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easy_site.settings')  # Asegúrate de cambiar 'myproject' por el nombre de tu proyecto

application = get_wsgi_application()
