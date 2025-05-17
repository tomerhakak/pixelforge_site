import os

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'accounts',
    'backend.leads.apps.LeadsConfig',
    'portfolio',
    'tasks',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # This path assumes settings.py is in backend/pixelforge/
        # and db.sqlite3 is in the project root, two levels up.
        'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db.sqlite3'),
    }
}

# If you have a BASE_DIR setting already defined, a cleaner way for 'NAME' would be:
# 'NAME': BASE_DIR / '..' / 'db.sqlite3', # if BASE_DIR points to 'backend'
# or 'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3') # if BASE_DIR points to 'backend'
# or 'NAME': os.path.join(BASE_DIR, 'db.sqlite3') # if BASE_DIR points to project root

# Email settings for development (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@pixelforge.example.com' # You can change this

# ... existing code ... 