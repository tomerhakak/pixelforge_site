from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.utils.translation import gettext_lazy as _ # Not strictly needed if title is hardcoded for check

from .models import Task
# IMPORTANT: Adjust this import based on your actual project structure!
# If 'leads' and 'tasks' are sibling apps:
from leads.models import Lead 
# If apps are under a 'pixelforge' directory that's a package:
# from pixelforge.leads.models import Lead
# If apps are under a 'backend' directory that's a package:
# from backend.leads.models import Lead


@receiver(post_save, sender=Task)
def auto_update_lead_status_on_task_completion(sender, instance, created, update_fields, **kwargs):
    print(f"--- TASK SIGNAL TRIGGERED: Task {instance.pk} (ID: {instance.id}) saved. ---")
    print(f"    Created: {created}, Completed: {instance.completed}, Title: '{instance.title}'")
    print(f"    update_fields: {update_fields}")

    # Ensure 'completed' field was part of the update and is now True.
    was_completed_field_updated_in_this_save = update_fields is not None and 'completed' in update_fields
    
    print(f"    Checking conditions: instance.completed ({instance.completed}), was_completed_field_updated_in_this_save ({was_completed_field_updated_in_this_save})")

    if instance.completed and was_completed_field_updated_in_this_save:
        print(f"    CONDITION 1 MET: Task is marked completed AND 'completed' field was in update_fields.")
        
        expected_title_start = "צור קשר ראשוני עם" # Using direct string
        print(f"    Checking title: instance.title ('{instance.title}') starts with '{expected_title_start}'?")

        if instance.title and instance.title.startswith(expected_title_start) and instance.lead:
            print(f"    CONDITION 2 MET: Title starts with '{expected_title_start}' AND task has a related lead.")
            
            print(f"    Checking lead status: Lead {instance.lead.pk} current status is '{instance.lead.status}'. Expected '{Lead.LeadStatus.NEW}'.")
            if instance.lead.status == Lead.LeadStatus.NEW:
                print(f"    CONDITION 3 MET: Lead status is NEW.")
                try:
                    instance.lead.status = Lead.LeadStatus.CONTACTED
                    instance.lead.save(update_fields=['status'])
                    print(f"    SUCCESS: Lead {instance.lead.pk} status updated to 'Contacted'.")
                except Exception as e:
                    print(f"    ERROR SAVING LEAD: Could not update lead {instance.lead.pk} status. Error: {e}")
            else:
                print(f"    SKIPPED: Lead {instance.lead.pk} status is not '{Lead.LeadStatus.NEW}', it is '{instance.lead.status}'. No update needed by this signal.")
        else:
            if not (instance.title and instance.title.startswith(expected_title_start)):
                print(f"    SKIPPED: Title mismatch. Task title '{instance.title}' does not start with '{expected_title_start}'.")
            if not instance.lead:
                print(f"    SKIPPED: Task {instance.pk} has no related lead.")
    else:
        if not instance.completed:
            print(f"    SKIPPED: Task {instance.pk} is not marked as completed.")
        if not was_completed_field_updated_in_this_save:
             print(f"    SKIPPED: 'completed' field was not in update_fields (was_completed_field_updated_in_this_save is False). This means 'completed' status didn't change in this save operation or was not specified as an updated field.") 