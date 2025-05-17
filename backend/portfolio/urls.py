from django.urls import path
from .views import ServiceListView, ProjectListView

app_name = 'portfolio'
 
urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
] 