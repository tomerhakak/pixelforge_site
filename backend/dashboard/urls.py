from django.urls import path
from .views import KpiView, RecentLeadsView, LeadsByStatusView

urlpatterns = [
    path('kpis/', KpiView.as_view(), name='dashboard-kpis'),
    path('recent-leads/', RecentLeadsView.as_view(), name='dashboard-recent-leads'),
    path('leads-by-status/', LeadsByStatusView.as_view(), name='dashboard-leads-by-status'),
] 