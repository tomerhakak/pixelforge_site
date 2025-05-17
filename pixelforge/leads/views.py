from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Lead
from .serializers import LeadSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from rest_framework.views import APIView

User = get_user_model()

class LeadViewSet(viewsets.ModelViewSet):
    """ 
    API endpoint that allows leads to be viewed or edited.
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

@method_decorator(csrf_exempt, name='dispatch')
class PublicLeadCreateView(generics.CreateAPIView):
    """
    Public API endpoint for creating leads.
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Assign to a specific user by username
        default_user_username = "tomer1997"
        try:
            assignee = User.objects.get(username=default_user_username)
            # You can assign to 'assigned_to' and/or 'created_by'
            serializer.save(assigned_to=assignee, created_by=assignee)
            print(f"--- PUBLIC LEAD: Lead created and assigned to {default_user_username} ---")
        except User.DoesNotExist:
            # Fallback: save without assignment or handle error differently
            serializer.save()
            print(f"--- PUBLIC LEAD WARNING: User {default_user_username} not found. Lead saved without specific assignment. ---")
        except Exception as e:
            # Handle other potential errors during save
            print(f"--- PUBLIC LEAD ERROR: Could not save lead with assignment. Error: {e} ---")
            # Option 1: Save without assignment as a fallback
            # serializer.save()
            # Option 2: Or, re-raise the exception or return an error response
            # For now, let's allow it to potentially fail if assignment fails critically
            # depending on how critical this assignment is.
            # If you want to guarantee lead creation even if user assignment fails, 
            # ensure a general .save() is called in an outer try/except or finally block,
            # or make the specific assignment part more robust.
            # Re-raising the error if the intention is for it to be a critical failure:
            # raise # This would make the API call fail if the user isn't found or other save error occurs.
            # For a robust system, you might want to log this error and still save the lead without assignment,
            # or assign to a default system user.
            # Current choice: If user tomer1997 is not found, it saves unassigned.
            # If another error happens during save(assigned_to=assignee...), it prints and does not save.
            # Let's make it save unassigned in case of other errors during the specific save too.
            try:
                serializer.save() # Fallback save
                print(f"--- PUBLIC LEAD INFO: Lead saved without specific assignment due to an error during assigned save. ---")
            except Exception as final_save_e:
                print(f"--- PUBLIC LEAD CRITICAL ERROR: Could not save lead at all. Error: {final_save_e} ---")
                # Here you might want to raise the exception to return a 500 error to the client
                # For now, it just prints.

# You might want a view to list leads for authenticated users
class LeadListView(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated] # Ensure only logged-in users can see

    def get_queryset(self):
        # Optionally filter leads based on the user (e.g., assigned_to or created_by)
        user = self.request.user
        # return Lead.objects.filter(assigned_to=user) # Example filter
        return Lead.objects.all() # Or just return all for now

    def perform_create(self, serializer):
        # Assign the logged-in user as the creator when a new lead is created via this view
        serializer.save(created_by=self.request.user)


# View for retrieving/updating/deleting a specific lead
class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated] # Only logged-in users
    # Add more specific permissions later if needed (e.g., only owner/assignee can modify)


# --- NEW VIEW FOR DASHBOARD --- 
class RecentLeadsListView(generics.ListAPIView):
    """Provides a list of the 5 most recently created leads."""
    queryset = Lead.objects.order_by('-created_at')[:5] # Get latest 5 leads
    serializer_class = LeadSerializer # Use the existing LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- NEW DASHBOARD VIEW --- 
class LeadsByStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Annotate leads with their status display name and count them
        # Assuming your Lead model has a 'status' field with choices
        # and you want to group by the actual status value (e.g., 'new', 'contacted')
        status_counts = (
            Lead.objects
            .values('status') # Group by the status field value
            .annotate(count=Count('status')) # Count occurrences of each status
            .order_by('status') # Optional: order by status value
        )
        
        # To get the display name for each status, you'd typically iterate
        # and use the model's _get_FIELD_display() method if needed, or map in serializer.
        # For simplicity here, we'll return the raw status values and counts.
        # The frontend can map these to display names if necessary.
        
        # If you have a STATUS_CHOICES defined in your model, you can map them here:
        # status_display_map = {choice[0]: choice[1] for choice in Lead.STATUS_CHOICES}
        # formatted_data = [
        #     {"status": status_display_map.get(item['status'], item['status']), "count": item['count"]}
        #     for item in status_counts
        # ]
        # return Response(formatted_data)
        
        return Response(status_counts) # Returns list like: [{'status': 'new', 'count': 5}, ...]

# --- END NEW DASHBOARD VIEW --- 