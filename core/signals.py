from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import clear_url_caches, get_resolver
from .models import Company
from .dynamic_router import generate_company_patterns

@receiver(post_save, sender=Company)
def update_company_urls(sender, instance, **kwargs):
    resolver = get_resolver()
    existing_patterns = resolver.url_patterns

    # Obtener las rutas raíz ('', 'admin/')
    root_patterns = [pattern for pattern in existing_patterns if pattern.pattern.describe() in ("''", "'admin/'")]

    # Generar nuevas rutas dinámicas
    companies = [company.name for company in Company.objects.all()]
    new_patterns = generate_company_patterns(companies)

    # Actualizar las rutas incluyendo las rutas raíz
    resolver.url_patterns = root_patterns + new_patterns
    clear_url_caches()
