from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Organization, SubscriptionPlan
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate

# Get the User model
User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=150)
    phone_number = serializers.CharField(required=False, max_length=20)
    organization_name = serializers.CharField(required=False, max_length=200)

    def to_internal_value(self, data):
        print(f"--- CustomRegisterSerializer to_internal_value - incoming data: {data} ---") # DEBUG
        if hasattr(data, 'copy'):
            processed_data = data.copy()
        else:
            processed_data = dict(data)

        # --- Re-add mapping for password_confirm to password2 --- 
        if 'password_confirm' in processed_data:
            confirm_val = processed_data.pop('password_confirm')
            # Ensure confirm_val is a string, not a list (can happen with QueryDict)
            processed_data['password2'] = confirm_val[0] if isinstance(confirm_val, list) else confirm_val
        # --------------------------------------------------------

        print(f"--- CustomRegisterSerializer to_internal_value - data passed to super: {processed_data} ---") # DEBUG ADDED
        return super().to_internal_value(processed_data)

    @transaction.atomic # Added @transaction.atomic for robustness
    def save(self, request):
        user = super().save(request)

        # --- Explicitly set username to email --- 
        if not user.username: # Set username only if it wasn't set by allauth (e.g., if USERNAME_REQUIRED was true before)
            user.username = user.email
            # Save username immediately if it was changed
            # user.save(update_fields=['username']) # Will be saved later with other fields
            print(f"--- REGISTRATION: Explicitly set username to {user.email} for user ID {user.pk} ---")
        # ---------------------------------------

        update_fields_list = []
        if not user.username: # if username was just set above
            user.username = user.email
            update_fields_list.append('username')

        user.first_name = self.validated_data.get('first_name', user.first_name or '')
        if self.validated_data.get('first_name') is not None: update_fields_list.append('first_name')
        
        user.last_name = self.validated_data.get('last_name', user.last_name or '')
        if self.validated_data.get('last_name') is not None: update_fields_list.append('last_name')

        phone_number = self.validated_data.get('phone_number')
        if phone_number:
            user.phone = phone_number
            update_fields_list.append('phone')

        organization_name = self.validated_data.get('organization_name')
        if organization_name:
            organization, org_created = Organization.objects.get_or_create(
                name=organization_name
            )
            user.organization = organization
            update_fields_list.append('organization')
            if org_created:
                 print(f"--- REGISTRATION: Created new organization '{organization_name}' ---")
            else:
                 print(f"--- REGISTRATION: Linked user to existing organization '{organization_name}' ---")
        
        if update_fields_list:
            user.save(update_fields=update_fields_list)
            print(f"--- REGISTRATION: User {user.email} updated with fields: {update_fields_list} ---")

        return user

# --- Add UserSerializer --- 
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, used for displaying user info."""
    class Meta:
        model = User # Use the User model imported at the top
        # Include fields you want to expose in the API
        fields = ['id', 'email', 'first_name', 'last_name'] 
        # Optionally make some fields read-only if they shouldn't be updated via this serializer
        read_only_fields = fields

# --- Optional: Add other serializers like OrganizationSerializer if needed --- 

class CustomLoginSerializer(RestAuthLoginSerializer):
    username = None  # We don't want username for this serializer
    email = forms.EmailField(required=True)
    # password field is inherited from RestAuthLoginSerializer

    def validate(self, attrs):
        print(f"--- CustomLoginSerializer VALIDATE: Received attrs: {attrs} ---") # DEBUG PRINT
        email = attrs.get('email')
        password = attrs.get('password')

        user = None
        if email and password:
            # Try to authenticate using Django's ModelBackend (which can often handle email as username)
            # or any other backend that might be configured and supports email.
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            # If the above fails, and you specifically want to target users by email field directly
            # (e.g., if username is something else or ModelBackend isn't finding it via email)
            if not user:
                try:
                    # Attempt to fetch the user by email directly
                    user_by_email = User.objects.get(email__iexact=email)
                    if user_by_email.check_password(password):
                        user = user_by_email
                except User.DoesNotExist:
                    pass # User with this email does not exist

        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        # If we got here, user is valid & active
        attrs['user'] = user
        return attrs