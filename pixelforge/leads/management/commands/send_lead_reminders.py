import logging
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from backend.leads.models import Lead
# from backend.tasks.models import Task # Uncomment if you want to create a task

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Scans for new leads that have not been touched and sends reminders.'

    def handle(self, *args, **options):
        reminder_hours = getattr(settings, 'LEAD_REMINDER_HOURS', 24)
        time_threshold = timezone.now() - timedelta(hours=reminder_hours)

        self.stdout.write(f"Scanning for new leads created before {time_threshold.strftime('%Y-%m-%d %H:%M:%S')} that need a reminder...")

        # Query for leads that are still 'new', created before the threshold, and have an assignee
        leads_to_remind = Lead.objects.filter(
            status=Lead.LeadStatus.NEW,
            created_at__lte=time_threshold,
            assigned_to__isnull=False # Ensure there is someone to send the reminder to
        ).select_related('assigned_to') # Optimize DB query by fetching related user

        if not leads_to_remind.exists():
            self.stdout.write(self.style.SUCCESS('No leads found requiring a reminder.'))
            return

        self.stdout.write(f'Found {leads_to_remind.count()} lead(s) to remind.')
        processed_count = 0

        for lead in leads_to_remind:
            # Optional: Add logic here to check if a reminder was sent recently for this lead
            # e.g., using a new DateTimeField 'last_reminder_sent_at' on the Lead model
            # For now, we send a reminder every time this command runs and finds them.

            assignee = lead.assigned_to
            if not assignee or not assignee.email:
                self.stdout.write(self.style.WARNING(f"Lead ID {lead.pk} is assigned to {assignee.username if assignee else 'N/A'} who has no email. Skipping reminder."))
                continue

            lead_name = f"{lead.first_name or ''} {lead.last_name or ''}".strip()
            if not lead_name:
                lead_name = f"Lead ID {lead.pk}"
            
            subject_prefix = getattr(settings, 'EMAIL_SUBJECT_PREFIX', '')
            subject = f"{subject_prefix}תזכורת: ליד '{lead_name}' ממתין לטיפול"
            
            html_message = f"""
            <p dir="rtl">שלום {assignee.first_name or assignee.username},</p>
            <p dir="rtl">זוהי תזכורת אוטומטית.</p>
            <p dir="rtl">הליד <strong>{lead_name}</strong> (ID: {lead.pk}) עדיין במצב 'חדש' וממתין לטיפולך מאז {lead.created_at.strftime('%Y-%m-%d %H:%M')}.</p>
            <p dir="rtl">פרטי הליד:</p>
            <ul>
                <li>שם: {lead_name}</li>
                <li>אימייל: {lead.email or 'לא סופק'}</li>
                <li>טלפון: {lead.phone_number or 'לא סופק'}</li>
            </ul>
            <p dir="rtl">אנא בדוק את המערכת וטפל בליד בהקדם.</p>
            <p dir="rtl">בברכה,</p>
            <p dir="rtl">מערכת PixelForge CRM</p>
            """
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL

            try:
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    [assignee.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f"Reminder email sent to {assignee.email} for Lead ID {lead.pk} ('{lead_name}')."))
                
                # Optional: Create a follow-up task for the reminder
                # task_title = f"תזכורת - המשך טיפול בליד {lead_name}"
                # task_description = f"משימת תזכורת אוטומטית: הליד {lead_name} (ID: {lead.pk}) עדיין חדש וממתין לטיפול."
                # due_date_task = timezone.now().date() + timedelta(days=1)
                # Task.objects.create(
                #     title=task_title,
                #     description=task_description,
                #     assigned_to=assignee,
                #     lead=lead,
                #     due_date=due_date_task
                # )
                # self.stdout.write(self.style.SUCCESS(f"Follow-up task created for Lead ID {lead.pk}."))

                # Optional: Update a 'last_reminder_sent_at' field on the lead
                # lead.last_reminder_sent_at = timezone.now()
                # lead.save(update_fields=['last_reminder_sent_at'])

                processed_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to send reminder for Lead ID {lead.pk}. Error: {e}"))

        self.stdout.write(f"Finished processing. {processed_count} reminder(s) sent.") 