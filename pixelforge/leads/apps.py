from django.apps import AppConfig

class LeadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Ensure this name matches how the 'leads' app is registered in INSTALLED_APPS
    # and how it's structured in your project (e.g., 'leads' or 'pixelforge.leads').
    name = 'pixelforge.leads' # Changed to reflect the full path as in INSTALLED_APPS
    label = 'leads' # Explicitly set the app label

    def ready(self):
        # Ensure signals are imported using the correct path relative to this app
        # or the project structure.
        from . import signals # Changed to relative import 