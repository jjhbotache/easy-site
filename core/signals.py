from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import clear_url_caches
from .models import Company
from .dynamic_router import generate_company_patterns

@receiver(post_save, sender=Company)
def update_company_urls(sender, instance, **kwargs):
    from django.conf import settings
    from django.urls import get_resolver

    companies = [company.name for company in Company.objects.all()]
    patterns = generate_company_patterns(companies)
    resolver = get_resolver()
    resolver.url_patterns = patterns
    clear_url_caches()
