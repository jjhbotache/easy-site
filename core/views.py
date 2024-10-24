from django.shortcuts import get_object_or_404, redirect, render
from core.logic.appointments_logic import create_appointment_logic, update_appointment_logic
from core.logic.helpers.logic_helpers import company_from_request, send_gmail
from core.logic.helpers.str_helpers import get_color_variations, get_company_name_from_url
from core.models import Appointment, Product, Company
from django.conf import settings
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from .models import Appointment, Company
import json

def home(request):
    company = company_from_request(request)
    
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    return render(request, 'pages/home.html', {
        "company": company,
        "colors": colors,
        "products": Product.objects.filter(company=company)
    })

def catalog(request):
    company = company_from_request(request)
    
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    return render(request, 'pages/catalog.html', {
        "company": company,
        "colors": colors,
        "products": Product.objects.filter(company=company)
    })

def us(request):
    company = company_from_request(request)
    
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    return render(request, 'pages/us.html', {
        "company": company,
        "colors": colors
    })

def contact(request):
    company = company_from_request(request)
    
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    return render(request, 'pages/contact.html', {
        "company": company,
        "colors": colors
    })

def product_detail(request, product_id):
    company = company_from_request(request)
    product = get_object_or_404(Product, id=product_id, company=company)
    
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    # treatment of product data
    product.features = [f.strip() for f in product.features.split(',')]
    product.price = f"{round(product.price*1000):,}".replace(",", ".")
    related_products = Product.objects.filter(company=company).exclude(id=product_id)
    
    
    return render(request, 'pages/product.html', {
        "company": company,
        "colors": colors,
        "product": product,
        "related_products": related_products,
    })

def calendar_view(request):
    company = company_from_request(request)
    appointments = list(Appointment.objects.filter(company=company).values())
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    calendar_config = {
        "appointment_duration": company.appointment_duration,
        "appointment_start_time": company.appointment_start_time,
        "appointment_end_time": company.appointment_end_time,
        "off_hours": company.off_hours,
        "off_days_of_the_week": company.off_days_of_the_week
    }
    
    return render(request, 'pages/calendar.html', {
        'appointments': appointments,
        "company": company,
        "colors": colors,
        "calendar_config": calendar_config
    })
    
def contact_through_mail(request):
    print('contact_through_mail')
    print(request)
    company = company_from_request(request)
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    if request.method == 'POST':
        # Leer datos enviados con POST
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        if settings.DEBUG:
            print(f"Simulated email to {company.email}")
            print(f"Subject: Mensaje de {nombre} desde {company.name} simplesite")
            print(f"Body: Nombre: {nombre}\nEmail: {email}\nMensaje: {mensaje}")
        else:
            send_gmail(
            recipient_email=company.email,
            subject=f"Mensaje de {nombre} desde {company.name} simplesite",
            body=f"Nombre: {nombre}\nEmail: {email}\nMensaje: {mensaje}"
            )
        return render(request, 'pages/contact_success.html', {
            "company": company,
            "colors": colors,
        })
    
    # redirect to home
    print('redirecting to home')
    redirect('/home')


# functon routes


def create_appointment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            company = company_from_request(request)
            response = create_appointment_logic(data, company)
        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'message_dict'):
                error_message = e.message_dict
            response = {
                'status': 'error',
                'message': error_message
            }
        return JsonResponse(response)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        try:
            company = company_from_request(request)
            response = update_appointment_logic(data, company)
        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'message_dict'):
                error_message = e.message_dict
            response = {
                'status': 'error',
                'message': error_message
            }
        return JsonResponse(response)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)