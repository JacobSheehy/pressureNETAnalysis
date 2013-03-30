import os

# Django settings for pressurenet project.

DEBUG = True 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pressurenet',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'TODO',
        'PASSWORD': 'TODO',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'served/media/')
STATIC_ROOT = os.path.join(PROJECT_PATH, 'served/static/')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

MAPS_API = 'TODO'
ANALYTICS_API = 'UA-78967-8'
PRESSURENET_DATA_URL = 'TODO' 

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static/'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'TODO'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/'),
)

READINGS_API_KEYS = [
]

