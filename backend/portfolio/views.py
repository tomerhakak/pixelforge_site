from rest_framework import generics, permissions # Import permissions if needed
from .models import Service, Project # Import Project
from .serializers import ServiceSerializer, ProjectSerializer # Import ProjectSerializer

# Create your views here.

class ServiceListView(generics.ListAPIView):
    """View to list all services, ordered by the 'order' field."""
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # For public view, show ALL services from ALL orgs
        return Service.objects.all().order_by('order')

# Add ProjectListView
class ProjectListView(generics.ListAPIView):
    """View to list all projects, ordered by the 'order' field."""
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

    # Override get_serializer_context to pass request to serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        # For public view, show ALL projects from ALL orgs
        return Project.objects.all().order_by('order')

# You might add ProjectListView later
# class ProjectListView(generics.ListAPIView):
#     queryset = Project.objects.all().order_by('order')
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.AllowAny] 

# Consider adding DetailViews later if needed (e.g., ServiceDetailView)
# class ServiceDetailView(generics.RetrieveAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = [permissions.AllowAny] # Or IsAuthenticated if details are private

# class ProjectDetailView(generics.RetrieveAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.AllowAny] # Or IsAuthenticated 