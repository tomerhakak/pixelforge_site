"""
crm_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # Ensure include is imported
# Add these for serving media files during development
from django.conf import settings
from django.conf.urls.static import static

# Import the custom view directly
from accounts.views import CustomRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/leads/', include('leads.urls')), # Include leads app URLs under api/leads/
    path('api/portfolio/', include('portfolio.urls')), # Include portfolio URLs
    path('api/tasks/', include('tasks.urls')), # Include tasks app URLs
    path('api/dashboard/', include('dashboard.urls')), # Include dashboard app URLs

    # dj-rest-auth URLs for login, logout, password reset, etc.
    path('api/auth/', include('dj_rest_auth.urls')),
    
    # Use CustomRegisterView directly for the registration endpoint
    path('api/auth/registration/', CustomRegisterView.as_view(), name='rest_register'), 
    
    # path('api/auth/registration/', include('accounts.urls')), # Previous attempt
    # path('api/auth/registration/', include('dj_rest_auth.registration.urls')), # Original default
]

# Add this for serving media files (like project images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 