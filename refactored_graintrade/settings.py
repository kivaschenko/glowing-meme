import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ij*e%-3@)7@bzlw9p8fc&m(yg-*m0azwj+lrxkwj6se6f2=9=8'

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get('DB_HOST', 'localhost'),
        "PORT": 54321,
    },
    "other": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "other",
        "USER": "geodjango",
    },
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # 3rd parties
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_gis',
    'dotenv',
    "celery",
    "django_celery_results",
    "django_celery_beat",
    'drf_spectacular',
    "crispy_forms",
    "crispy_bootstrap5",
    "storages",
    # local
    'offers.apps.OffersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'refactored_graintrade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR / 'templates'),
        ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'refactored_graintrade.wsgi.application'
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

DEFAULT_FILE_STORAGE = 'refactored_graintrade.storage_backends.AzureMediaStorage'
STATICFILES_STORAGE = 'refactored_graintrade.storage_backends.AzureStaticStorage'

STATIC_LOCATION = "staticfiles"
MEDIA_LOCATION = "mediafiles"

AZURE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY_1')
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('CACHES_LOCATION'),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": os.environ.get('CACHES_KEY_PREFIX'),
    },
}

# Logger
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {'format': '[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s',},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "log_to_stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "offers": {
            "handlers": ["log_to_stdout"],
            "level": "INFO",
            "propagate": True,
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        # }
    },
    "root": {
        "handlers": ["log_to_stdout"],
        "level": "INFO",
    }
}


LOGOUT_REDIRECT_URL = "home"
LOGIN_REDIRECT_URL = "home"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# Mapbox
MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoia2l2YXNjaGVua28iLCJhIjoiY2xva2dweG41MjR0aDJxbWVibTFid3VndyJ9._Gia54L_MbRbTl99ZilRXw"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
# Celery Configuration Options
CELERY_IMPORTS = (
    "offers.tasks",
)
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_CACHE_BACKEND = 'default'
CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

SPECTACULAR_SETTINGS = {
    'TITLE': 'Graintrade Refactored API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}
