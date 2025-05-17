from django.contrib import admin
# from django.utils.translation import gettext_lazy as _ # Not strictly needed here
from .models import Lead

# Register your models here.

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    # Use display_name, include phone_number, use created_at instead of timestamp? Check model fields.
    list_display = ('display_name', 'email', 'phone_number', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'created_at', 'assigned_to') # Use created_at
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'description', 'assigned_to__email') # Add phone, description, search by team name
    list_editable = ('status', 'assigned_to') # Allow editing more fields in list view
    date_hierarchy = 'created_at' # Use created_at
    readonly_fields = ('created_at', 'modified_at') # Make both timestamps read-only
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'phone_number') # Main contact info
        }),
        ('סטטוס וניהול', { # Section for status and assignment
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('תיאור', { # Description section
            'fields': ('description',),
            'classes': ('collapse',), # Collapsible section
        }),
        ('מטא נתונים', { # Metadata section
            'fields': ('created_at', 'modified_at', 'created_by'),
            'classes': ('collapse',),
        }),
    )

    # Remove old commented out display methods if not needed

    # Example for explicit column header translation (usually not needed)
    # @admin.display(description=_('כתובת אימייל'), ordering='email')
    # def email_display(self, obj):
    #     return obj.email
    #
    # @admin.display(description=_('שם'), ordering='name')
    # def name_display(self, obj):
    #     return obj.name
    #
    # @admin.display(description=_('חותמת זמן'), ordering='timestamp')
    # def timestamp_display(self, obj):
    #     return obj.timestamp 