from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import Company, Product, User,Appointment

class ProductAdmin(admin.ModelAdmin):
    # list_display = ('name', 'company', 'price')

    # Filtrar para que el usuario solo vea productos de su empresa
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:  # Si es superusuario, ve todo
            return qs
        return qs.filter(company=request.user.company)  # Solo productos de su empresa

    # Asignar automáticamente la compañía del usuario que crea el producto
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:  # Si no es superusuario
            obj.company = request.user.company  # Asignar la compañía del usuario
        super().save_model(request, obj, form, change)

    # Eliminar el campo 'company' del formulario si no es superusuario
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:  # Si no es superusuario, ocultar el campo
            form.base_fields.pop('company', None)  # Remover el campo 'company'
        return form


class CompanyAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:  # Si es superusuario, ve todo
            return qs
        return qs.filter(name=request.user.company)  # Solo su empresa

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.id = request.user.company.id
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields.pop('id', None)
            form.base_fields.pop('owner', None)  # Remover el campo 'owner'
        return form

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['owner']  # Hacer el campo 'owner' de solo lectura
        return super().get_readonly_fields(request, obj)
        

class AppointmentAdmin(admin.ModelAdmin):
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('company', 'start_datetime', 'end_datetime')
        return ('start_datetime', 'end_datetime')
    search_fields = ('full_name', 'email', 'phone_number', 'message')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:  # Si es superusuario, ve todo
            return qs
        return qs.filter(company=request.user.company)  # Solo productos de su empresa

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:  # Si no es superusuario
            obj.company = request.user.company  # Asignar la compañía del usuario
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:  # Si no es superusuario, ocultar el campo
            form.base_fields.pop('company', None)  # Remover el campo 'company'
        return form

admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Appointment, AppointmentAdmin)