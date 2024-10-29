from django.shortcuts import get_object_or_404, redirect, render
from core.logic.appointments_logic import create_appointment_logic, delete_appointment_logic, update_appointment_logic
from core.logic.helpers.logic_helpers import company_from_request, send_gmail
from core.logic.helpers.str_helpers import get_color_variations, get_company_name_from_url
from core.models import Appointment, Product, Company
from django.conf import settings
from django.http import JsonResponse, HttpResponse
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
    """
    Renders the calendar view for the company.
    This view performs the following actions:
    - Retrieves the company from the request.
    - Fetches the list of appointments for the company.
    - Prepares the color configuration for the calendar based on the company's settings.
    - Prepares the calendar configuration including appointment duration, start and end times, off hours, and off days of the week.
    - Identifies if the user is authenticated (admin).
    User Permissions:
    - If the user is not an admin:
        - Hide the cancel token from the appointments.
        - Hide specific appointment information.
        - Allow the user to create appointments.
        - Do not allow the user to update appointments.
        - Do not allow the user to delete appointments.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered calendar page with the context including appointments, company, colors, and calendar configuration.
    """
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
    
    # identify if the user is an admin
    is_admin = request.user.is_authenticated
    
    if not is_admin:
        # only left the fields that are needed for the user
        appointments = [ {
                "id": appointment["id"],
                "start_datetime": appointment["start_datetime"],
                "end_datetime": appointment["end_datetime"],
            } for appointment in appointments ]
        
            
    
    print(is_admin)
    return render(request, 'pages/calendar.html', {
        'appointments': appointments,
        "company": company,
        "colors": colors,
        "calendar_config": calendar_config,
        "is_admin": is_admin
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
        print(data)
        try:
            company = company_from_request(request)
            response = create_appointment_logic(data, company)
        except Exception as e:
            error_message = str(e)
            print(e)
            if hasattr(e, 'message_dict'):
                error_message = e.message_dict
            response = {
                'status': 'error',
                'message': error_message
            }
        return JsonResponse(response)
    elif request.method == 'PUT':
        # only allow to company admins to update appointments
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
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

def cancel_appointment(request, token):
    
    data = json.loads(request.body) if request.body else {}
    data["cancel_token"] = token
    delete_appointment_logic(
        data,
        company_from_request(request),
        message=  "(Cita cancelada por el cliente.)" if request.method == "GET" else data.get('message')
    )
    # if it was a get, return a success message, other wise return a json response
    return HttpResponse("Cita cancelada con éxito." if request.method == "GET" else JsonResponse({'status': 'success'}))