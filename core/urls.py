from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .logic.helpers.str_helpers import txt_to_url
from .models import Company
from .views import home, catalog, about, contact, contact_through_mail

try: 
    companies = [txt_to_url(company.name) for company in Company.objects.all()]
    
    patterns = [
        *[path(f'{company}/', home, name="home") for company in companies],
        *[path(f'{company}/catalogo', catalog, name="catalog") for company in companies],
        *[path(f'{company}/nosotros', about, name="about") for company in companies],
        *[path(f'{company}/contacto', contact, name="contact") for company in companies],
        *[path(f'{company}/contact-through-mail', contact_through_mail) for company in companies],
    ]
except:
    patterns = []
finally:
    urlpatterns = [
        *patterns,
    ]