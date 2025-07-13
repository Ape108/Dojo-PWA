from django.contrib import admin
from .models import Belt, BeltGroup, Technique, SupplementalMaterial
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.conf import settings

@admin.register(BeltGroup)
class BeltGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'color')
    ordering = ('display_order',)

@admin.register(Belt)
class BeltAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'display_order', 'color')
    list_filter = ('group',)
    ordering = ('display_order',)

    inlines = [] # Initialize inlines to an empty list

@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'belt', 'order_in_belt', 'video_enabled')
    list_filter = ('belt',)
    search_fields = ('name', 'description')
    ordering = ('belt__display_order', 'order_in_belt')
    list_editable = ('video_enabled',)


class SupplementalMaterialInlineForm(forms.ModelForm):
    class Meta:
        model = SupplementalMaterial
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(config_name='supplemental_inline'),
        }

class SupplementalMaterialInline(admin.TabularInline):
    model = SupplementalMaterial
    extra = 1
    form = SupplementalMaterialInlineForm
    fields = ('title', 'material_type', 'file', 'external_url', 'content', 'display_order', 'thumbnail', 'description')
    readonly_fields = ()

    class Media:
        css = {
            'all': ('admin/supplemental_inline.css',)
        }

# CKEditor config for maximize button and larger size
if not hasattr(settings, 'CKEDITOR_CONFIGS'):
    settings.CKEDITOR_CONFIGS = {}
settings.CKEDITOR_CONFIGS['supplemental_inline'] = {
    'toolbar': 'full',
    'height': 300,
    'width': '700px',
    'extraPlugins': 'maximize',
    'removePlugins': 'resize',
}

@admin.register(SupplementalMaterial)
class SupplementalMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'belt', 'material_type', 'display_order', 'created_at')
    list_filter = ('material_type', 'belt')
    search_fields = ('title', 'description', 'content')
    ordering = ('belt', 'display_order', 'title')

# Add the inline to the Belt admin
BeltAdmin.inlines = [SupplementalMaterialInline] + list(getattr(BeltAdmin, 'inlines', []))

