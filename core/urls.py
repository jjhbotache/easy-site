from django.contrib import admin
from django.urls import path
from .views import home, catalog, us, contact, contact_through_mail, product_detail, calendar_view, create_appointment, cancel_appointment

urlpatterns = [
    path('<str:company_name>/', home, name="home"),
    path('<str:company_name>/catalogo', catalog, name="catalog"),
    path('<str:company_name>/nosotros', us, name="about"),
    path('<str:company_name>/contacto', contact, name="contact"),
    path('<str:company_name>/contact-through-mail', contact_through_mail),
    path('<str:company_name>/producto/<int:product_id>/', product_detail, name="product_detail"),
    path('<str:company_name>/calendario', calendar_view, name="calendar"),
    path('<str:company_name>/create-appointment/', create_appointment, name="create_appointment"),
    path('<str:company_name>/cancel-appointment/<uuid:token>/', cancel_appointment, name='cancel_appointment'),
]