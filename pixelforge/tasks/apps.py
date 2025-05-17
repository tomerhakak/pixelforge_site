from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Adjust the name based on your project structure.
    # If 'tasks' is a direct sub-app of 'backend' (where manage.py might be),
    # then name should likely be 'tasks' or 'backend.tasks'.
    # Assuming 'pixelforge' is a common root directory for apps that is on the PYTHONPATH.
    name = 'tasks' 

    def ready(self):
        # Import signals here to connect them when the app is ready.
        # Adjust the import path based on your project structure.
        import tasks.signals 