from rest_framework import serializers
from .models import Lead
# from accounts.serializers import UserSerializer # Import UserSerializer
from backend.accounts.serializers import UserSerializer # Corrected import

class LeadSerializer(serializers.ModelSerializer):
    # Include nested serializers for related fields
    created_by = UserSerializer(read_only=True)
    # assigned_to = UserSerializer(read_only=True) # Keep if you want the full user object
    
    # Fields for frontend compatibility / specific needs
    owner_username = serializers.CharField(source='assigned_to.username', read_only=True, allow_null=True)
    owner_email = serializers.CharField(source='assigned_to.email', read_only=True, allow_null=True) # If you also want email easily accessible
    message = serializers.CharField(source='description', read_only=True, allow_null=True)
    phone = serializers.CharField(source='phone_number', read_only=True, allow_null=True)

    display_name = serializers.CharField(read_only=True) 
    status_display = serializers.CharField(read_only=True)

    class Meta:
        model = Lead
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            # 'phone_number', # Replaced by 'phone'
            'phone',
            # 'description',  # Replaced by 'message'
            'message',
            'status',
            'status_display',
            'priority',
            # 'assigned_to', # Keep if you want the full user object, or rely on owner_username/owner_email
            'owner_username',
            'owner_email', # Added for completeness, frontend model uses it
            'created_by', 
            'created_at', 
            'modified_at',
            'display_name', 
        )
        # Update read_only fields to reflect current model state
        read_only_fields = (
            'id', 
            'created_by', 
            'created_at', 
            'modified_at', 
            'display_name', 
            'status_display',
            'owner_username',
            'owner_email',
            'message', # as it's sourced from description
            'phone',   # as it's sourced from phone_number
        )
        # Note: assigned_to might be writable depending on your logic elsewhere 