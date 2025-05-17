from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'lead', 'assigned_to', 'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'due_date', 'assigned_to')
    search_fields = ('title', 'description', 'lead__first_name', 'lead__last_name')
    date_hierarchy = 'due_date' 