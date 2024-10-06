from django.shortcuts import render
from core.logic.helpers.str_helpers import get_color_variations, get_company_name_from_url
from core.models import Product, Company



def home(request):
    company_text = get_company_name_from_url(request.get_full_path())
    company = Company.objects.filter(name__icontains=company_text).order_by('name')[0]
    colors = {
        "background_color": company.background_color,
        "text_color": company.text_color,
        "primary_color": get_color_variations(company.primary_color),
        "secondary_color": get_color_variations(company.secondary_color)
    }
    
    
    return render(request, 'pages/home.html',{
        "company": company,
        "colors":colors,
        "products": Product.objects.filter(company=company)
    })
