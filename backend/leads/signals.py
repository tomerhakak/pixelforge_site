from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Lead
from django.contrib.auth import get_user_model # Import User model
from backend.tasks.models import Task # Import Task model
from django.utils import timezone # For due_date
from datetime import timedelta # For due_date

User = get_user_model()

# Placeholder - REPLACE WITH YOUR ACTUAL CALENDLY LINK
DEFAULT_CALENDLY_LINK = "https://calendly.com/your-username/meeting-type"

@receiver(post_save, sender=Lead)
def notify_new_lead(sender, instance, created, **kwargs):
    if created:
        original_assigned_to = instance.assigned_to
        assigned_sales_rep_email = None
        assigned_user_for_task = None # User for task creation

        # Automatically assign to 'tomer1997' if no one is assigned
        if not instance.assigned_to:
            try:
                default_assignee = User.objects.get(username='tomer1997') # Or use email if preferred and unique
                # Modify the instance in memory, don't save here to avoid recursion if this signal is re-triggered
                instance.assigned_to = default_assignee 
                assigned_user_for_task = default_assignee
                print(f"ליד '{instance.display_name}' שויך אוטומטית (בזיכרון) ל: {default_assignee.email}")
                if default_assignee.email:
                    assigned_sales_rep_email = default_assignee.email
            except User.DoesNotExist:
                print(f"שגיאה: המשתמש 'tomer1997' המיועד לשיוך אוטומטי לא נמצא.")
            except Exception as e:
                print(f"שגיאה בשיוך אוטומטי של ליד: {e}")
        elif instance.assigned_to:
            assigned_user_for_task = instance.assigned_to
            if instance.assigned_to.email:
                assigned_sales_rep_email = instance.assigned_to.email
        
        # If the instance.assigned_to was changed in this signal (because it was initially None)
        # and the initial save was from PublicLeadCreateView where created_by and assigned_to were set,
        # we might not need to save instance again here if the view's save persists it.
        # However, PublicLeadCreateView calls serializer.save() which triggers this signal.
        # The assignment to default_owner happens in PublicLeadCreateView *before* this signal.
        # So instance.assigned_to should already be default_owner if it came from PublicLeadCreateView.

        # Re-check assigned_user_for_task based on the instance that came into the signal
        # This logic might need refinement based on when PublicLeadCreateView sets assigned_to vs when this signal fires.
        # For now, assume instance.assigned_to is correctly set by the view if coming from there.
        if instance.assigned_to:
            assigned_user_for_task = instance.assigned_to 
            if instance.assigned_to.email: # For email notification
                 assigned_sales_rep_email = instance.assigned_to.email


        from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'webmaster@localhost'

        # --- Notify Sales Representative ---
        if assigned_sales_rep_email:
            subject_rep = f"ליד חדש נוצר: {instance.display_name}"
            message_lines_rep = [
                f"ליד חדש נוצר במערכת:",
                f"שם: {instance.display_name}",
                f"אימייל: {instance.email}",
                f"טלפון: {instance.phone_number if instance.phone_number else 'לא צוין'}",
                f"תיאור: {instance.description if instance.description else 'לא צוין'}",
                f"סטטוס: {instance.get_status_display()}",
                f"עדיפות: {instance.get_priority_display()}",
            ]
            if instance.assigned_to:
                message_lines_rep.append(f"משויך ל: {instance.assigned_to.get_full_name()} ({instance.assigned_to.email})")
            else:
                message_lines_rep.append("לא משויך לאף אחד")
            
            message_rep = "\n".join(message_lines_rep)
            try:
                send_mail(
                    subject_rep,
                    message_rep,
                    from_email,
                    [assigned_sales_rep_email],
                    fail_silently=False,
                )
                print(f"התראת אימייל על ליד חדש נשלחה אל איש המכירות: {assigned_sales_rep_email}")
            except Exception as e:
                print(f"שגיאה בשליחת אימייל לאיש מכירות על ליד חדש: {e}")
        else:
            # Fallback if no one is assigned and auto-assignment failed or assigned user has no email
            # This part might need review based on desired fallback behavior
            print(f"אזהרה: לא נשלחה התראה לאיש מכירות עבור הליד {instance.display_name}. בדוק את הגדרות השיוך והאימייל של המשתמשים.")
            # Consider sending to a default admin email here if necessary
            # default_admin_email = 'admin@example.com'
            # send_mail(...)


        # --- Notify Lead with Calendly Link ---
        if instance.email: # Ensure lead has an email
            subject_lead = f"ברוך הבא ל-Pixelforge, {instance.first_name or instance.display_name}!"
            # You can customize the Calendly link further, e.g., per sales rep if needed
            calendly_link_to_use = DEFAULT_CALENDLY_LINK 
            if instance.assigned_to and hasattr(instance.assigned_to, 'profile') and hasattr(instance.assigned_to.profile, 'calendly_link') and instance.assigned_to.profile.calendly_link:
                # Assuming a user profile model might store individual calendly links
                # For now, this part is hypothetical.
                # calendly_link_to_use = instance.assigned_to.profile.calendly_link
                pass


            message_lead = f"""שלום {instance.first_name or instance.display_name},

תודה על התעניינותך ב-Pixelforge!
אנו שמחים לצרף אותך ורוצים להבין איך נוכל לעזור לך בצורה הטובה ביותר.

נשמח לקבוע איתך שיחה קצרה בזמנך הפנוי.
תוכל לקבוע פגישה ישירות דרך הקישור הבא:
{calendly_link_to_use}

אם יש לך שאלות נוספות לפני כן, אל תהסס להשיב למייל זה.

בברכה,
צוות Pixelforge
"""
            try:
                send_mail(
                    subject_lead,
                    message_lead,
                    from_email,
                    [instance.email],
                    fail_silently=False,
                )
                print(f"אימייל ברוכים הבאים עם קישור לקלנדלי נשלח לליד: {instance.email}")
            except Exception as e:
                print(f"שגיאה בשליחת אימייל ברוכים הבאים לליד ({instance.email}): {e}")
        else:
            print(f"אזהרה: לליד {instance.display_name} אין כתובת אימייל. לא נשלח אימייל ברוכים הבאים.")

        # --- Create a follow-up task for the new lead ---
        if assigned_user_for_task and assigned_user_for_task.organization:
            task_title = f"Follow up with new lead: {instance.display_name}"
            try:
                Task.objects.create(
                    title=task_title,
                    description=f"New lead created: {instance.display_name} ({instance.email}).\\nNotes: {instance.description}",
                    assigned_to=assigned_user_for_task,
                    created_by=assigned_user_for_task, # Must be a valid user
                    organization=assigned_user_for_task.organization, # Must be a valid org
                    lead=instance,
                    priority=Task.PRIORITY_CHOICES[1][0], # Medium priority ('medium')
                    due_date=timezone.now() + timedelta(days=2),
                    status=Task.STATUS_CHOICES[0][0] # 'todo'
                )
                print(f"--- AUTO-TASK CREATED (NEW SIGNAL): Task '{task_title}' for Lead {instance.pk} ---")
            except Exception as e:
                print(f"--- AUTO-TASK ERROR (NEW SIGNAL): Failed to create task for Lead {instance.pk}. Error: {e} ---")
        elif not assigned_user_for_task:
            print(f"--- AUTO-TASK SKIPPED (NEW SIGNAL): Lead {instance.pk} has no assigned user for task creation. ---")
        elif not assigned_user_for_task.organization:
            print(f"--- AUTO-TASK SKIPPED (NEW SIGNAL): Assigned user {assigned_user_for_task.email} for lead {instance.pk} has no organization. ---")


# New signal handler for creating tasks
@receiver(post_save, sender=Lead)
def create_task_on_lead_status_change(sender, instance, created, **kwargs):
    if not created: # Only run on updates, not on creation
        # Check if the status is one that should trigger a task
        if instance.status in [Lead.CONTACTED, Lead.INPROGRESS]:
            if instance.assigned_to and instance.assigned_to.organization:
                task_title = f"לקבוע פגישה עם {instance.display_name}"
                
                # Check if a similar open task already exists for this lead
                existing_tasks = Task.objects.filter(
                    lead=instance,
                    title=task_title,
                    status__in=[Task.STATUS_CHOICES[0][0], Task.STATUS_CHOICES[1][0]] # 'todo' or 'in_progress'
                )
                
                if not existing_tasks.exists():
                    try:
                        Task.objects.create(
                            title=task_title,
                            description=f"יש לקבוע פגישת המשך עם הליד: {instance.display_name} ({instance.email}).\nפרטי הליד: {instance.description}",
                            assigned_to=instance.assigned_to,
                            created_by=instance.assigned_to, # Or a system user
                            organization=instance.assigned_to.organization,
                            lead=instance,
                            priority=Task.PRIORITY_CHOICES[2][0], # High priority ('high')
                            due_date=timezone.now() + timedelta(days=3),
                            status=Task.STATUS_CHOICES[0][0] # 'todo'
                        )
                        print(f"משימה אוטומטית '{task_title}' נוצרה עבור {instance.assigned_to.email} עקב שינוי סטטוס של ליד.")
                    except Exception as e:
                        print(f"שגיאה ביצירת משימה אוטומטית עבור ליד {instance.display_name}: {e}")
                else:
                    print(f"משימה פתוחה '{task_title}' כבר קיימת עבור ליד {instance.display_name}. לא נוצרה משימה חדשה.")
            else:
                if not instance.assigned_to:
                    print(f"אוטומציה ליצירת משימה: ליד {instance.display_name} אינו משויך לאף אחד.")
                elif not instance.assigned_to.organization:
                    print(f"אוטומציה ליצירת משימה: למשתמש {instance.assigned_to.email} המשויך לליד {instance.display_name} אין ארגון משויך.") 