from django.contrib import admin
from .models import Belt, Technique

@admin.register(Belt)
class BeltAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    ordering = ('display_order',)

@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'belt', 'order_in_belt')
    list_filter = ('belt',)
    search_fields = ('name', 'description')
    ordering = ('belt__display_order', 'order_in_belt')

