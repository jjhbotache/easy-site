from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Company

@receiver(post_save, sender=Company)
def update_company_urls(sender, instance, **kwargs):
    # No longer needed to update URL patterns dynamically
    pass
