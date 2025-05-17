from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task, TaskComment, TaskAttachment
from .serializers import TaskSerializer, TaskCommentSerializer, TaskAttachmentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the tasks
        for the currently authenticated user's organization.
        Optionally filters by lead_id if provided in query_params.
        """
        user_organization = getattr(self.request.user, 'organization', None)
        if not user_organization:
            return Task.objects.none()  # Return empty queryset if no organization

        queryset = Task.objects.filter(organization=user_organization)
        
        # Allow filtering by created_by for potential admin/overview scenarios
        # Or perhaps filter by organization if you implement multi-tenancy
        # For now, let's consider if a user can see tasks they created OR are assigned to them
        # queryset = Task.objects.filter(models.Q(assigned_to=user) | models.Q(created_by=user)).distinct()

        lead_id = self.request.query_params.get('lead_id')
        if lead_id is not None:
            queryset = queryset.filter(lead_id=lead_id)
            
        return queryset.order_by('-due_date', 'priority')

    def perform_create(self, serializer):
        user_organization = getattr(self.request.user, 'organization', None)
        if not user_organization:
            raise serializers.ValidationError(
                {"organization": "User must be associated with an organization to create a task."}
            )
        
        serializer.save(
            created_by=self.request.user,
            organization=user_organization
        )

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        task = self.get_object()
        serializer = TaskCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_attachment(self, request, pk=None):
        task = self.get_object()
        serializer = TaskAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return Response(self.get_serializer(task).data)
        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )

class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_organization = getattr(self.request.user, 'organization', None)
        if not user_organization:
            return TaskComment.objects.none()
        return TaskComment.objects.filter(
            task__organization=user_organization
        )

class TaskAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_organization = getattr(self.request.user, 'organization', None)
        if not user_organization:
            return TaskAttachment.objects.none()
        return TaskAttachment.objects.filter(
            task__organization=user_organization
        ) 