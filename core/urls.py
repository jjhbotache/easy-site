from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .logic.helpers.str_helpers import txt_to_url
from .models import Company
from .views import cancel_appointment, home, catalog, us, contact, contact_through_mail, product_detail, calendar_view, create_appointment

try: 
    companies = [txt_to_url(company.name) for company in Company.objects.all()]
    
    patterns = [
        *[path(f'{company}/', home, name="home") for company in companies],
        *[path(f'{company}/catalogo', catalog, name="catalog") for company in companies],
        *[path(f'{company}/nosotros', us, name="about") for company in companies],
        *[path(f'{company}/contacto', contact, name="contact") for company in companies],
        *[path(f'{company}/contact-through-mail', contact_through_mail) for company in companies],
        *[path(f'{company}/producto/<int:product_id>/', product_detail, name="product_detail") for company in companies],
        *[path(f'{company}/calendario', calendar_view, name="calendar") for company in companies],
        *[path(f'{company}/create-appointment/', create_appointment, name="create_appointment") for company in companies],
        *[path(f'{company}/cancel-appointment/<uuid:token>/', cancel_appointment, name='cancel_appointment') for company in companies],
        
    ]
except:
    patterns = []
finally:
    urlpatterns = [
        *patterns,
    ]