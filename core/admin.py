from django.contrib import admin
from .models import Company, Product, User

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'price')

    # Filtrar para que el usuario solo vea productos de su empresa
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:  # Si es un superusuario, ve todo
            return qs
        return qs.filter(company=request.user.company)  # Solo productos de su empresa

    # Asignar automáticamente la compañía del usuario que crea el producto
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:  # Si no es superusuario
            obj.company = request.user.company  # Asignar la compañía del usuario
        super().save_model(request, obj, form, change)

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Product, ProductAdmin)
