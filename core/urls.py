from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .dynamic_router import generate_company_patterns
from .models import Company

companies = [company.name for company in Company.objects.all()]
urlpatterns = generate_company_patterns(companies) + [
    # path('admin/', admin.site.urls),
    # ... other static patterns ...
]