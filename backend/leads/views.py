from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView # Added for LeadsByStatusView
from django.db.models import Count # Added for LeadsByStatusView
from .models import Lead
# from backend.accounts.models import UserProfile, Organization # UserProfile removed
from backend.accounts.models import Organization # Organization is still needed if used directly elsewhere
from .serializers import LeadSerializer
from django.contrib.auth import get_user_model # Import User model
from django.shortcuts import get_object_or_404 # Import get_object_or_404
# --- Imports for Task Automation ---
from backend.tasks.models import Task # Corrected import path
from django.utils import timezone
from datetime import timedelta
from django.db import models
# --- End Imports ---

User = get_user_model() # Get the active User model

# --- LeadViewSet (copied from pixelforge/leads/views.py, queryset might need adjustment) ---
class LeadViewSet(viewsets.ModelViewSet):
    """ 
    API endpoint that allows leads to be viewed or edited.
    """
    # queryset = Lead.objects.all() # Original queryset
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Filter leads based on the user's organization. """
        user = self.request.user
        organization = user.organization
        if organization:
            users_in_org = User.objects.filter(organization=organization)
            return Lead.objects.filter(
               models.Q(assigned_to__in=users_in_org) | models.Q(created_by__in=users_in_org)
            ).distinct()
        else:
            return Lead.objects.none()
    
    def perform_create(self, serializer):
        """ Set created_by to the requesting user and potentially assigned_to if logic dictates. """
        # Example: Assign to current user by default if not otherwise specified
        # Ensure `assigned_to` is handled based on your application's logic
        # For a ModelViewSet, create is handled by the serializer if assigned_to is writable.
        # If you need specific logic, override the create method or perform_create.
        serializer.save(created_by=self.request.user)

# View to list leads (can be removed if LeadViewSet handles list adequately)
class LeadListView(generics.ListAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        organization = user.organization
        if organization:
            users_in_org = User.objects.filter(organization=organization)
            return Lead.objects.filter(
               models.Q(assigned_to__in=users_in_org) | models.Q(created_by__in=users_in_org)
            ).distinct()
        else:
            return Lead.objects.none()

# View to create leads (can be removed if LeadViewSet handles create adequately)
class LeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        requesting_user = self.request.user
        serializer.save(created_by=requesting_user, assigned_to=requesting_user)

# View for lead details (can be removed if LeadViewSet handles retrieve/update/destroy adequately)
class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        organization = user.organization
        if organization:
            users_in_org = User.objects.filter(organization=organization)
            return Lead.objects.filter(
               models.Q(assigned_to__in=users_in_org) | models.Q(created_by__in=users_in_org)
            ).distinct()
        else:
            return Lead.objects.none()

# Public view for lead creation
class PublicLeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        default_owner_email = 'tomerhakak15@gmail.com' # Ensure this user exists
        default_owner = None
        try:
            default_owner = User.objects.get(email=default_owner_email)
        except User.DoesNotExist:
            print(f"CRITICAL WARNING: Default owner for public leads '{default_owner_email}' not found! Lead saved without owner.")
            serializer.save() # Save without owner if default not found
            return
        serializer.save(assigned_to=default_owner, created_by=default_owner)
        print(f"Public lead {serializer.instance.id} created, assigned to {default_owner.email}")


# --- Dashboard Views (copied from pixelforge/leads/views.py) --- 
class RecentLeadsListView(generics.ListAPIView):
    """Provides a list of the 5 most recently created leads."""
    # queryset = Lead.objects.order_by('-created_at')[:5]
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Filter recent leads based on the user's organization. """
        user = self.request.user
        organization = user.organization
        base_queryset = Lead.objects.order_by('-created_at')
        if organization:
            users_in_org = User.objects.filter(organization=organization)
            return base_queryset.filter(
               models.Q(assigned_to__in=users_in_org) | models.Q(created_by__in=users_in_org)
            ).distinct()[:5]
        else:
            # If no org, maybe show only user's unassigned recent leads or none
            return Lead.objects.none() 

class LeadsByStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        organization = user.organization
        
        queryset = Lead.objects.all()
        if organization:
            users_in_org = User.objects.filter(organization=organization)
            queryset = queryset.filter(
               models.Q(assigned_to__in=users_in_org) | models.Q(created_by__in=users_in_org)
            ).distinct()
        else:
            queryset = Lead.objects.none()
            
        status_counts = (
            queryset
            .values('status') 
            .annotate(count=Count('status')) 
            .order_by('status') 
        )
        return Response(status_counts)
    