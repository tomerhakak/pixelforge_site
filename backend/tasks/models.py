from django.db import models
from django.conf import settings
from django.utils import timezone
from backend.leads.models import Lead
from backend.accounts.models import Organization
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    completed = models.BooleanField(_("Completed"), default=False)
    completed_at = models.DateTimeField(_("Completed At"), blank=True, null=True)
    lead = models.ForeignKey(
        Lead,
        related_name='tasks',
        on_delete=models.CASCADE, # If Lead deleted, delete associated tasks
        null=True,
        blank=True, # Allow tasks not linked to a specific lead
        verbose_name=_("Related Lead")
    )

    class Meta:
        ordering = ['-created_at']
        app_label = 'tasks' # Explicitly define the app_label
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically set completed_at when status is set to done
        if self.status == 'done' and not self.completed:
            self.completed = True # Keep completed field for now, might be useful
            if self.completed_at is None:
                 self.completed_at = timezone.now()
        elif self.status != 'done':
            self.completed = False
            self.completed_at = None
        super().save(*args, **kwargs)

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.task.title}'

class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Attachment for {self.task.title}' 