from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics # Import generics
from django.utils import timezone # Import timezone for task filtering if needed
from django.db.models import Count # Import Count for aggregation

# Import models from other apps
from leads.models import Lead
from portfolio.models import Project, Service
from tasks.models import Task

# Import serializers
from leads.serializers import LeadSerializer # Assuming LeadSerializer exists and is suitable

class KpiView(APIView):
    """API view to provide Key Performance Indicator data for the dashboard."""
    permission_classes = [permissions.IsAuthenticated] # Requires user to be logged in

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Calculate KPIs - Adjust logic as needed (e.g., filter by organization)
        total_leads = Lead.objects.count() # Or filter by user/organization
        total_projects = Project.objects.count() # Or filter
        total_services = Service.objects.count() # Or filter
        
        # User-specific KPIs
        user_tasks_total = Task.objects.filter(assigned_to=user).count()
        user_tasks_due = Task.objects.filter(assigned_to=user, completed=False, due_date__isnull=False).count() # Count non-completed tasks with a due date
        user_tasks_completed_today = Task.objects.filter(
            assigned_to=user, 
            completed=True, 
            # completed_at__date=timezone.now().date() # Need to import timezone
        ).count() # Example: add logic for completed today

        kpi_data = {
            'total_leads': total_leads,
            'total_projects': total_projects,
            'total_services': total_services,
            'my_tasks_total': user_tasks_total,
            'my_tasks_due': user_tasks_due,
            # Add more KPIs as needed
        }
        
        return Response(kpi_data, status=status.HTTP_200_OK)

# --- New View for Recent Leads ---
class RecentLeadsView(generics.ListAPIView):
    """API view to provide a list of the most recent leads."""
    serializer_class = LeadSerializer # Use your existing LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Optional: Add pagination if needed
    # pagination_class = None # Or some pagination class

    def get_queryset(self):
        """Return the 5 most recently created leads (adjust filtering as needed)."""
        user = self.request.user
        # TODO: Filter leads based on user/organization if necessary
        # Example: return Lead.objects.filter(organization=user.userprofile.organization).order_by('-created_at')[:5]
        # Use 'created_at' which exists in the model, instead of 'timestamp'
        return Lead.objects.order_by('-created_at')[:5]

# --- New View for Leads by Status Chart Data ---
class LeadsByStatusView(APIView):
    """API view to provide data for the leads by status pie chart."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # TODO: Filter leads based on user/organization if necessary
        queryset = Lead.objects.all() 

        # Group by status and count leads in each status
        # Make sure the field name 'status' matches your Lead model
        status_counts = queryset.values('status').annotate(count=Count('id')).order_by('-count')
        
        chart_data = list(status_counts)

        return Response(chart_data, status=status.HTTP_200_OK) 