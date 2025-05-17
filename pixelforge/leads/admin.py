from django.contrib import admin
from .models import Lead

# Register your models here.

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_display_name', 'email', 'phone_number', 'status', 'priority', 'assigned_to', 'created_at')
    list_display_links = ('id', 'get_display_name')
    list_filter = ('status', 'priority', 'assigned_to', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'description')
    readonly_fields = ('created_at', 'modified_at', 'get_display_name')

    def get_display_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        elif obj.first_name:
            return obj.first_name
        elif obj.last_name:
            return obj.last_name
        elif obj.email:
            return obj.email
        return f"Lead {obj.pk}"
    get_display_name.short_description = 'Display Name'

    # Add other configurations as needed 