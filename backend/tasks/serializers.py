from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task, TaskComment, TaskAttachment
# from accounts.serializers import UserDetailsSerializer # Removed unused import
# from leads.serializers import LeadSerializer # Removed unused import

User = get_user_model()

class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField()

    class Meta:
        model = TaskAttachment
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['uploaded_by', 'uploaded_at']

class TaskCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = TaskComment
        fields = ['id', 'content', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    assigned_to = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assigned_to', 'created_by', 'due_date', 'created_at',
            'updated_at', 'comments', 'attachments'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set created_by to the request user automatically
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data) 