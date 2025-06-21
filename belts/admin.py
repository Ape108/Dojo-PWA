from django.contrib import admin
from .models import Belt, BeltGroup, Technique

@admin.register(BeltGroup)
class BeltGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'color')
    ordering = ('display_order',)

@admin.register(Belt)
class BeltAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'display_order', 'color')
    list_filter = ('group',)
    ordering = ('display_order',)

@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'belt', 'order_in_belt', 'video_enabled')
    list_filter = ('belt',)
    search_fields = ('name', 'description')
    ordering = ('belt__display_order', 'order_in_belt')
    list_editable = ('video_enabled',)

