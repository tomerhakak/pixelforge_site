from django.urls import path
from .views import CustomRegisterView

urlpatterns = [
    path('', CustomRegisterView.as_view(), name='rest_register'), # Use the same name as dj-rest-auth for consistency
] 