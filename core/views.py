from django.shortcuts import get_object_or_404, redirect, render
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
    appointments = Appointment.objects.all()
    appointments = list(Appointment.objects.all().values())
    company = company_from_request(request)
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    
    return render(request, 'pages/calendar.html', {
        'appointments': appointments,
        "company": company,
        "colors": colors,
        "calendar_config": {
            "appointment_duration": .25 #1 - .5 - .25
        }
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
            company = Company.objects.get(id=data['company_id'])
            start_datetime = parse_datetime(data['start_datetime'])
            end_datetime = parse_datetime(data['end_datetime'])
            appointment = Appointment.objects.create(
                company=company,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                full_name=data['full_name'],
                email=data.get('email', ''),
                phone_number=data.get('phone_number', ''),
                message=data.get('message', '')
            )
            response = {
                'status': 'success',
                'appointment_id': appointment.id
            }
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
        return JsonResponse(response)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)