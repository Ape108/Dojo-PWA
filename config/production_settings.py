# config/production_settings.py
from .settings import * # Inherit from the main settings file
import os

# --- Production Database ---
# (Your existing DATABASES setting is here)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': f'/cloudsql/{os.environ.get("CLOUD_SQL_CONNECTION_NAME")}',
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASS"),
        'NAME': os.environ.get("DB_NAME"),
    }
}


# --- Other Production Settings ---
DEBUG = False
ALLOWED_HOSTS = ['*'] # This is okay for Cloud Run

# --- ADD THIS SETTING ---
# Add your live service URL to the list of trusted origins for CSRF protection.
CSRF_TRUSTED_ORIGINS = ['https://dojo-pwa-service-849037756424.us-central1.run.app']