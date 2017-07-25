#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dj_database_url
import warnings

from wger.settings_global import *

# Use 'DEBUG = True' to get more details for server errors
DEBUG = os.environ.get("DEBUG") or True
TEMPLATES[0]['OPTIONS']['debug'] = True

ADMINS = (
    ('Your name', 'your_email@example.com'),
)
MANAGERS = ADMINS


DATABASES = {}
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'] = db_from_env


# DATABASES['default'] =  dj_database_url.config(default='postgres://foo:bar@somehost.amazonaws.com:5432/somedb')

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY", "2vhrp=0n5y#1kns*c)foi%d98qr#yn#3+=bm+c29qzkfu7ai(5")

# Your reCaptcha keys
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", "")
NOCAPTCHA = os.environ.get("NOCAPTCHA", True)

# The site's URL (e.g. http://www.my-local-gym.com or http://localhost:8000)
# This is needed for uploaded files and images (exercise images, etc.) to be
# properly served.
SITE_URL = os.environ.get("SITE_URL", "http://localhost:8000")

# Path to uploaded files
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Allow all hosts to access the application. Change if used in production.
ALLOWED_HOSTS = '*'

# This might be a good idea if you setup memcached
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Configure a real backend in production
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Sender address used for sent emails
WGER_SETTINGS['EMAIL_FROM'] = 'wger Workout Manager <wger@example.com>'

# Your twitter handle, if you have one for this instance.
#WGER_SETTINGS['TWITTER'] = ''

if os.path.exists(os.path.join(BASE_DIR, "wger/local_settings.py")):
    from .local_settings import *
else:
    warnings.warn("local_settings.py not found, using defaults")
