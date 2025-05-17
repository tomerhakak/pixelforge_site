from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Lead(models.Model):
    # Basic Info
    first_name = models.CharField(_("First Name"), max_length=100, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=100, blank=True, null=True)
    # Assuming email might be needed, adding based on serializer/admin common fields
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)

    # Status & Priority (Choices need to be defined)
    # Example choices - adjust as needed
    class LeadStatus(models.TextChoices):
        NEW = 'new', _('New')
        CONTACTED = 'contacted', _('Contacted')
        QUALIFIED = 'qualified', _('Qualified')
        LOST = 'lost', _('Lost')
        WON = 'won', _('Won')

    class LeadPriority(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        blank=True, null=True # Allow blank/null based on admin screenshot?
    )
    priority = models.CharField(
        _("Priority"),
        max_length=10,
        choices=LeadPriority.choices,
        default=LeadPriority.MEDIUM,
        blank=True, null=True # Allow blank/null based on admin screenshot?
    )

    # Ownership & Timestamps
    # Assuming assigned_to refers to a User
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_leads',
        on_delete=models.SET_NULL, # Keep lead if user is deleted? Adjust as needed.
        null=True,
        blank=True,
        verbose_name=_("Assigned To")
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_leads',
        on_delete=models.SET_NULL, # Keep lead if creator is deleted?
        null=True,
        blank=True, # Assuming created_by might not always be set?
        verbose_name=_("Created By")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return f"Lead {self.pk}"

    # Provides the display value for choice fields (used in serializer)
    def get_status_display(self):
        return dict(self.LeadStatus.choices).get(self.status)

    def get_priority_display(self):
        return dict(self.LeadPriority.choices).get(self.priority)

    class Meta:
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")
        ordering = ['-created_at'] # Default ordering 