from django.urls import path
from .views import home, catalog, us, contact, contact_through_mail, product_detail, calendar_view, create_appointment, cancel_appointment

def generate_company_patterns(companies):
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
    return patterns
