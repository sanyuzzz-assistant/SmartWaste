from django.contrib import admin
from django.utils.html import format_html

from .models import WasteCategory, WasteDetection


@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'is_recyclable',
    )

    list_filter = (
        'is_recyclable',
    )

    search_fields = (
        'name',
    )


@admin.register(WasteDetection)
class WasteDetectionAdmin(admin.ModelAdmin):

    list_display = (
        'image_preview',
        'user',
        'predicted_category',
        'confidence',
        'is_recyclable',
        'created_at',
    )

    list_filter = (
        'predicted_category',
        'created_at',
    )

    search_fields = (
        'user__username',
    )

    readonly_fields = (
        'created_at',
        'image_preview',
    )

    def image_preview(self, obj):
        if obj.uploaded_image:
            return format_html(
                '<img src="{}" width="80" height="80" '
                'style="object-fit:cover;border-radius:8px;" />',
                obj.uploaded_image.url
            )
        return "No Image"

    image_preview.short_description = 'Image'

    def is_recyclable(self, obj):
        if obj.predicted_category:
            return obj.predicted_category.is_recyclable
        return False

    is_recyclable.boolean = True
    is_recyclable.short_description = 'Recyclable'