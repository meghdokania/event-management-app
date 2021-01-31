from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# from .models import CustomUser

CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    """Define admin model for custom CustomUser model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ['name', 'institute', 'year']}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
    ordering = ('email',)