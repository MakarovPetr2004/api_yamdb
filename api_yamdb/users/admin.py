from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff',)
    list_display += ('get_role_display', 'groups',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)
    list_of_editable_models = ['Group']


admin.site.register(User, CustomUserAdmin)
