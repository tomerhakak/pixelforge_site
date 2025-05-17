from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.tasks' # Using the full path relative to the project root
    label = 'tasks'      # Explicitly setting the app label

    def ready(self):
        # Import signals here if you have them in tasks app
        # For example:
        # import backend.tasks.signals
        pass # No signals to import for now 