from django.apps import AppConfig


class LeadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.leads' # Changed back to 'backend.leads'

    def ready(self):
        import backend.leads.signals # This should still work as Python path should handle it 