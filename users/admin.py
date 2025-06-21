from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Add our custom fields to the admin display
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        # Add 'is_staff' here for easy access
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # Keep your custom section
        ('Dojo Information', {'fields': ('user_type', 'is_approved')}),
    )
    list_display = ('username', 'email', 'user_type', 'is_approved', 'is_staff')
    list_filter = ('user_type', 'is_approved', 'is_staff')
    # Allow admins to approve users directly from the list view
    list_editable = ('user_type', 'is_approved')
    
