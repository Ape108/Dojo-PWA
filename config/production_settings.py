# config/production_settings.py
from .settings import * # Inherit from the main settings file
import os
import dj_database_url

# --- Production Security ---
DEBUG = False
# For better security, you should replace '*' with your actual domain name.
ALLOWED_HOSTS = ['dojo-pwa-service-849037756424.us-central1.run.app']
CSRF_TRUSTED_ORIGINS = ['https://dojo-pwa-service-849037756424.us-central1.run.app']
X_FRAME_OPTIONS = 'SAMEORIGIN'

# --- HTTPS Settings for Proxy ---
# Trust the 'X-Forwarded-Proto' header from the proxy to determine if a request is secure.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Redirect all non-HTTPS requests to HTTPS.
SECURE_SSL_REDIRECT = True


# --- Production Database ---
# This is loaded correctly because the DJANGO_SETTINGS_MODULE is set in the cloud environment.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': f'/cloudsql/{os.environ.get("CLOUD_SQL_CONNECTION_NAME")}',
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASS"),
        'NAME': os.environ.get("DB_NAME"),
    }
}


# --- Media and Static Files Configuration (Corrected for Django 5.2+) ---

# Get the bucket name from the environment variable we set during deployment.
GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")

# This is the modern and correct way to configure storages in Django.
STORAGES = {
    # This configures how user-uploaded files (like PDFs and videos) are handled.
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            # This is the critical line. It tells django-storages which bucket to use.
            "bucket_name": GS_BUCKET_NAME,
            # This sets the default permissions for uploaded files to be publicly readable.
            "default_acl": "publicRead",
        },
    },
    # This configures how your application's static files (CSS, JS) are handled.
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# This setting tells Django where to find the static files that Whitenoise will serve.
STATIC_ROOT = BASE_DIR / "staticfiles"

# This setting tells the browser where to request the static files from.
STATIC_URL = "/static/"
