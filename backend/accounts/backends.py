from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL using email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # dj_rest_auth with allauth email login passes 'email' in kwargs or directly.
        # The 'username' parameter here is mostly for Django admin compatibility.
        auth_email = kwargs.get('email')  # Prioritize email from kwargs if passed directly
        if auth_email is None:
            auth_email = username # Fallback to username if email kwarg isn't there (e.g. from admin)

        print(f"--- EmailBackend: Trying to authenticate with email: {auth_email} (derived from username/kwargs) ---") # DEBUG
        
        if auth_email is None:
            print("--- EmailBackend: Email for authentication is None, returning None ---") # DEBUG
            return None
        
        try:
            # Case-insensitive lookup
            print(f"--- EmailBackend: Looking up user by email__iexact: {auth_email} ---") # DEBUG
            user = UserModel.objects.get(email__iexact=auth_email)
            print(f"--- EmailBackend: Found user: {user} ---") # DEBUG
        except UserModel.DoesNotExist:
            print(f"--- EmailBackend: User with email {auth_email} DoesNotExist ---") # DEBUG
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
            return None
        except MultipleObjectsReturned:
             print(f"--- EmailBackend: Multiple users found for email {auth_email} ---") # DEBUG
             # This shouldn't happen if emails are unique, but handle defensively.
             # You might want to log this occurrence.
             return None
        
        print(f"--- EmailBackend: Checking password for user {user}...") # DEBUG
        password_valid = user.check_password(password)
        print(f"--- EmailBackend: Password valid: {password_valid} ---") # DEBUG
        user_can_auth = self.user_can_authenticate(user)
        print(f"--- EmailBackend: User can authenticate: {user_can_auth} ---") # DEBUG
        
        if password_valid and user_can_auth:
            print(f"--- EmailBackend: Authentication successful for {user}, returning user ---") # DEBUG
            return user
        
        print("--- EmailBackend: Password or user check failed, returning None ---") # DEBUG
        return None

    def get_user(self, user_id):
        # This method is required by the backend API
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None 