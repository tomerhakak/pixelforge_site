from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField(read_only=True)  # Add display_name property
    status_display = serializers.SerializerMethodField(read_only=True)  # Add status_display property

    class Meta:
        model = Lead
        fields = [
            'id',
            'first_name',
            'last_name',
            'email', # Added email field
            'phone_number', # Added field
            'description',
            'status',
            'priority',
            'created_by', # Changed from owner:organization
            'created_at', # Changed from owner:organization
            'modified_at',
            'assigned_to', # Added field based on comment
            # Computed fields
            'display_name',
            'status_display',
        ]
        # update read_only fields to reflect current model state
        read_only_fields = [
            'id', # pk is read-only
            'created_by',
            'created_at',
            'modified_at',
            'display_name',
            'status_display'
        ]

    # Note: assigned_to might be writable depending on your logic elsewhere

    def get_display_name(self, obj):
        """Combines first and last name into a display name."""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        elif obj.first_name:
            return obj.first_name
        elif obj.last_name:
            return obj.last_name
        return "Unnamed Lead" # Or some other placeholder

    def get_status_display(self, obj):
        return obj.get_status_display() 