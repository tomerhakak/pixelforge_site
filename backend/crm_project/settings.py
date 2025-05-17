from pathlib import Path # Add this import

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent # Define BASE_DIR


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s=t#fnpv(l5@pfe*8j0kjs!vf2)43*53^zlg_a9@$&19_wxe7d' # You should replace this with your actual key from the original file if possible

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Required by allauth

    # Local Apps First (potentially problematic dependencies)
    'accounts',
    'backend.tasks',
    'backend.portfolio',
    'pixelforge.leads',
    'dashboard',

    # 3rd Party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the allauth middleware!
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'crm_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'crm_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Settings
# For development, allow all origins. Tighten this for production!
CORS_ALLOW_ALL_ORIGINS = True # Temporarily allow all for debugging

# Alternatively, be more specific:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:54461", # Flutter dev server - Keep commented for now
#     "http://127.0.0.1:54461",
#     # Add other origins if needed (e.g., "https://yourdomain.com")
# ]

# Optional: Consider if credentials (like cookies) need to be allowed
# CORS_ALLOW_CREDENTIALS = True

# Optional: Allow specific methods if needed (Defaults are usually sufficient)
# CORS_ALLOW_METHODS = [
# ... existing code ...
# Optional: Allow specific headers if needed (Defaults are usually sufficient)
# CORS_ALLOW_HEADERS = [
# ... existing code ...

# Add CSRF trusted origins for Flutter dev server
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000", # Default for Django dev server
    "http://127.0.0.1:8000",
    "http://localhost:8080", # Common alternative
    "http://127.0.0.1:8080",
    "http://localhost:5000", # Another common one
    "http://127.0.0.1:5000",
    # Add any specific Flutter dev ports you observe, e.g.:
    # "http://localhost:63779",
    # "http://127.0.0.1:63779",
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User' # ADDED: Point to our custom user model

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# dj-rest-auth settings
REST_AUTH = {
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
}

# allauth settings - Final adjustment to remove W001 warning
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
ACCOUNT_EMAIL_VERIFICATION = 'none'
# Set login method strictly to email to avoid conflict warning
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # Keep None
ACCOUNT_PASSWORD_MIN_LENGTH = 8
# Keep simplified list - RegisterSerializer defines actual requirements
ACCOUNT_SIGNUP_FIELDS = ['email', 'password']

# Add Authentication Backends for allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Must set SITE_ID for allauth
SITE_ID = 1

# Email Settings (Development - Prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
DEFAULT_FROM_EMAIL = 'info@pixelforge.co.il'  # Changed to a more specific example
EMAIL_SUBJECT_PREFIX = '[PixelForge CRM] ' # Optional prefix

# Any other settings below...