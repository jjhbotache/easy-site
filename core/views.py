from django.shortcuts import render
from core.logic.helpers.str_helpers import get_company_name_from_url
from core.models import Product, Company

def home(request):
    company_text = get_company_name_from_url(request.get_full_path())
    company = Company.objects.filter(name__icontains=company_text).order_by('name')[0]
    
    
    return render(request, 'pages/home.html',{
        "company": company,
        "products": Product.objects.filter(company=company)
    })
