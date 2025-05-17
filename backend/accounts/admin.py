from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization, SubscriptionPlan, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'organization', 'subscription_plan', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'organization', 'subscription_plan')
    search_fields = ('username', 'email', 'organization__name')
    ordering = ('username',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',) 