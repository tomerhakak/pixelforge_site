from django.db import models
from backend.accounts.models import Organization # Changed to full path
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.


class Lead(models.Model):
    # Define status choices
    NEW = 'new'
    CONTACTED = 'contacted'
    INPROGRESS = 'inprogress'
    LOST = 'lost'
    WON = 'won'

    CHOICES_STATUS = (
        (NEW, _('חדש')),
        (CONTACTED, _('נוצר קשר')),
        (INPROGRESS, _('בתהליך')),
        (LOST, _('אבוד')),
        (WON, _('זכיה'))
    )

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW, _('נמוכה')),
        (MEDIUM, _('בינונית')),
        (HIGH, _('גבוהה'))
    )

    # Core Fields based on edits so far
    first_name = models.CharField(_('שם פרטי'), max_length=255)
    last_name = models.CharField(_('שם משפחה'), max_length=255, blank=True, null=True)
    email = models.EmailField(_('אימייל'), unique=True)
    phone_number = models.CharField(_('מספר טלפון'), max_length=20, blank=True, null=True) # The newly added field
    description = models.TextField(_('תיאור'), blank=True, null=True)
    status = models.CharField(_('סטטוס'), max_length=15, choices=CHOICES_STATUS, default=NEW)
    priority = models.CharField(_('עדיפות'), max_length=15, choices=CHOICES_PRIORITY, default=MEDIUM)
    
    # Relationship Fields (ensure these match what you intend)
    # Assuming you want assigned_to and created_by, but maybe not owner/organization directly?
    # owner = models.ForeignKey(...) # REMOVED - If needed, use assigned_to or created_by
    # organization = models.ForeignKey(...) # REMOVED - Link through User or another model if needed
    
    assigned_to = models.ForeignKey(User, verbose_name=_("משוייך ל"), related_name='assigned_leads', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name=_("נוצר על ידי"), related_name='created_leads', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamp fields
    # message = models.TextField(...) # REMOVED - As it was in the original Traceback but not in desired state
    # timestamp = models.DateTimeField(...) # REMOVED - Replaced by created_at/modified_at
    created_at = models.DateTimeField(_('נוצר בתאריך'), auto_now_add=True)
    modified_at = models.DateTimeField(_('עודכן בתאריך'), auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("ליד")
        verbose_name_plural = _("לידים")

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name or self.last_name else self.email

    # Adding a computed property for title as used in dashboard serializer - keep if needed
    # @property
    # def title(self):
    #     name = f"{self.first_name or ''} {self.last_name or ''}".strip()
    #     return name if name else self.email

    @property
    def display_name(self):
        # Ensure both parts are strings or handle None
        fname = self.first_name if self.first_name else ''
        lname = self.last_name if self.last_name else ''
        full_name = f"{fname} {lname}".strip()
        return full_name if full_name else self.email # Return email if name is empty

    @property
    def status_display(self):
        return self.get_status_display()


class InteractionLog(models.Model):
    INTERACTION_CHOICES = [
        ('call', _('שיחה טלפונית')),
        ('meeting', _('פגישה')),
        ('email', _('אימייל')),
        ('chat', _('צ\'אט')),
        ('other', _('אחר')),
    ]

    lead = models.ForeignKey(Lead, related_name='interactions', on_delete=models.CASCADE, verbose_name=_("ליד משויך"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lead_interactions', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("נציג"))
    interaction_type = models.CharField(_("סוג אינטראקציה"), max_length=15, choices=INTERACTION_CHOICES, default='call')
    timestamp = models.DateTimeField(_("תאריך ושעת אינטראקציה"), default=timezone.now)
    notes = models.TextField(_("סיכום האינטראקציה"))
    duration_minutes = models.PositiveIntegerField(_("משך בדקות (אופציונלי)"), null=True, blank=True)
    next_step_notes = models.TextField(_("הערות לצעד הבא (אופציונלי)"), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = _("יומן אינטראקציה")
        verbose_name_plural = _("יומני אינטראקציות")

    def __str__(self):
        return f"{self.get_interaction_type_display()} עם {self.lead.display_name} בתאריך {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
