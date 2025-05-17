import uuid  # Required for UUIDs
from django.db import models
# from django.contrib.auth.models import User # REMOVE: We are creating a custom User model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser, Group, Permission # ADD: Imports for custom User
from django.utils.translation import gettext_lazy as _
# from django.db.models.signals import post_save # REMOVE: No longer needed for UserProfile
# from django.dispatch import receiver # REMOVE: No longer needed for UserProfile


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=255, help_text="Organization Name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# REMOVE UserProfile and its signal receiver
# class UserProfile(models.Model):
#     ... (UserProfile code removed) ...
# @receiver(post_save, sender=User) # REMOVE (User will be our custom model)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     ... (signal code removed) ...


# ADD: Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not full_name:
            raise ValueError(_('The Full Name field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN) # Default superuser to ADMIN role

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('role') != User.Role.ADMIN:
            raise ValueError(_('Superuser must have role=ADMIN.'))
            
        return self.create_user(email, full_name, password, **extra_fields)

# ADD: Custom User Model
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        SALES = 'SALES', _('Sales')
        VIEWER = 'VIEWER', _('Viewer')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('כתובת אימייל'), unique=True)
    full_name = models.CharField(_('שם מלא'), max_length=255)
    phone = models.CharField(_('מספר טלפון'), max_length=20, blank=True, null=True)
    role = models.CharField(
        _('תפקיד'),
        max_length=10,
        choices=Role.choices,
        default=Role.VIEWER # Default role, can be adjusted
    )
    
    is_active = models.BooleanField(_('פעיל?'), default=True)
    is_staff = models.BooleanField(_('חבר צוות?'), default=False) # Required for Django admin access
    # is_superuser field is inherited from PermissionsMixin

    created_at = models.DateTimeField(_('נוצר בתאריך'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name'] # Fields required when creating user via createsuperuser

    class Meta:
        verbose_name = _('משתמש')
        verbose_name_plural = _('משתמשים')

    def __str__(self):
        return self.email

    # We can add a property for organization if we decide to link it directly later
    # @property
    # def organization(self):
    #     # Logic to get organization if linked, e.g., through a OneToOneField or ForeignKey
    #     return None 