from django.contrib import admin
from django.utils.translation import gettext_lazy as _ # Import if needed
from .models import Service, Project #, Testimonial

# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description', 'technologies')
    list_filter = ('technologies',)

# Uncomment if using Testimonial model
# @admin.register(Testimonial)
# class TestimonialAdmin(admin.ModelAdmin):
#     list_display = ('author_name', 'quote', 'order')
#     list_editable = ('order',)
#     search_fields = ('quote', 'author_name', 'author_title') 