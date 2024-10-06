from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from .logic.helpers.str_helpers import txt_to_url
from .models import Company
from .views import home
# for each company, we will have a landing page

try: 
    urlpatterns = [
        path(f'{txt_to_url(company.name)}/', home)
        for company in Company.objects.all()
    ]
except:
    urlpatterns = []


