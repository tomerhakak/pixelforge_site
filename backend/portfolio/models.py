from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _ # Import gettext_lazy
from backend.accounts.models import Organization # Changed to full path to avoid conflict

# Create your models here.

class Service(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name=_("ארגון"), null=True)
    title = models.CharField(_("כותרת"), max_length=100)
    description = models.TextField(_("תיאור"))
    # Consider choices for icons if using a specific library like FontAwesome
    # icon = models.CharField(max_length=50, help_text="e.g., 'fas fa-code' for FontAwesome")
    # Or use an ImageField if you want to upload custom icons:
    # icon_image = models.ImageField(upload_to='service_icons/', blank=True, null=True)
    icon_identifier = models.CharField(
        _("מזהה אייקון"),
        max_length=100,
        help_text=_("לדוגמה: 'fas fa-code' או 'desktop' (לפי FontAwesome)")
    )
    order = models.PositiveIntegerField(
        _("סדר תצוגה"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("מספר נמוך יופיע ראשון")
    )

    class Meta:
        ordering = ['organization', 'order', 'title'] # Add org to ordering
        verbose_name = _("שירות")
        verbose_name_plural = _("שירותים")

    def __str__(self):
        org_name = _("ללא ארגון") if self.organization is None else self.organization.name
        return f'{self.title} ({org_name})'

class Project(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name=_("ארגון"), null=True)
    title = models.CharField(_("כותרת"), max_length=150)
    description = models.TextField(_("תיאור"))
    image = models.ImageField(_("תמונה"), upload_to='project_images/', blank=True, null=True)
    link = models.URLField(_("קישור"), blank=True, null=True)
    technologies = models.CharField(
        _("טכנולוגיות"),
        max_length=200,
        blank=True,
        help_text=_("רשימת טכנולוגיות מופרדת בפסיק")
    )
    order = models.PositiveIntegerField(
        _("סדר תצוגה"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("מספר נמוך יופיע ראשון")
    )

    class Meta:
        ordering = ['organization', 'order', 'title'] # Add org to ordering
        verbose_name = _("פרויקט")
        verbose_name_plural = _("פרויקטים")

    def __str__(self):
        org_name = _("ללא ארגון") if self.organization is None else self.organization.name
        return f'{self.title} ({org_name})'

# Optional: Testimonial model
# class Testimonial(models.Model):
#     quote = models.TextField()
#     author_name = models.CharField(max_length=100)
#     author_title = models.CharField(max_length=100, blank=True)
#     order = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], help_text="Lower numbers appear first")
# 
#     class Meta:
#         ordering = ['order', 'author_name']
# 
#     def __str__(self):
#         return f'"{self.quote[:30]}..." - {self.author_name}' 