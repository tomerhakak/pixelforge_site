from django.urls import path, include
# from rest_framework.routers import DefaultRouter # Comment out router
from .views import LeadViewSet, PublicLeadCreateView, RecentLeadsListView, LeadsByStatusView

# router = DefaultRouter()
# router.register(r'leads', LeadViewSet, basename='lead')

# Define paths relative to the include prefix ('api/leads/')
urlpatterns = [
    # Base path '/' within 'api/leads/' for list and general create
    path('', LeadViewSet.as_view({'get': 'list', 'post': 'create'}), name='lead-list'),
    # Path 'public-create/' within 'api/leads/'
    path('public-create/', PublicLeadCreateView.as_view(), name='lead-public-create'),
    # Path '<int:pk>/' within 'api/leads/'
    path('<int:pk>/', LeadViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='lead-detail'),
    # URL for creating public leads (e.g., from a website form)
    path('dashboard/recent/', RecentLeadsListView.as_view(), name='dashboard_recent_leads'),
    path('dashboard/leads-by-status/', LeadsByStatusView.as_view(), name='dashboard_leads_by_status'),
] 