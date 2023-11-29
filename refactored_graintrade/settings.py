import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

DEBUG = os.environ.get("DEBUG")
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get('DB_HOST', 'localhost'),
        "PORT": 5432,
    },
    "other": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "other",
        "USER": "test-user",
    },
}

SITE_ID = 1
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']
SITE_HOST = os.environ.get('SITE_HOST')
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
    # 'rest_framework_simplejwt',
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

# STATIC_URL = 'static/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "refactored_graintrade/static")
# STATIC_URL = "staticfiles/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [
#     BASE_DIR / 'staticfiles',
# ]
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "remote_storage": {
        "BACKEND": "refactored_graintrade.storage_backends.PublicMediaStorage",
        "OPTIONS": {
            "session_profile": '',
            "access_key": '',
            "secret_key": '',
            "region_name": 'nyc3',
            "endpoint_url": 'https://nyc3.digitaloceanspaces.com',
        }
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

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


# TIME_ZONE = "America/New_York"
# SITE_HOST = "https://some-production-domain.com"

# CSRF_TRUSTED_ORIGINS = ["https://*", "http://*/"]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# Mapbox
MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoia2l2YXNjaGVua28iLCJhIjoiY2xva2dweG41MjR0aDJxbWVibTFid3VndyJ9._Gia54L_MbRbTl99ZilRXw"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    #     # 'rest_framework.permissions.IsAuthenticated',
    #     # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
# Celery Configuration Options
CELERY_IMPORTS = (
    "offers.tasks",
)
CELERY_TIMEZONE = "Europe/Kyiv"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_CACHE_BACKEND = 'default'
CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
#
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
#
# AWS_S3_ENDPOINT_URL = "https://{}".format(os.environ.get("AWS_S3_ENDPOINT_URL"))
# AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
# }
# AWS_LOCATION = f"{AWS_STORAGE_BUCKET_NAME}/staticfiles"
# AWS_DEFAULT_ACL = "public-read"
#
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
#
# STATIC_URL = f"{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
#
# # public mediafiles settings
# PUBLIC_MEDIA_LOCATION = f"{AWS_STORAGE_BUCKET_NAME}/mediafiles"
# MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/"
# DEFAULT_FILE_STORAGE = "core.storage_backends.PublicMediaStorage"
# # private mediafiles settings
# PRIVATE_MEDIA_LOCATION = f"{AWS_STORAGE_BUCKET_NAME}/private"
# PRIVATE_FILE_STORAGE = "core.storage_backends.PrivateMediaStorage"

SPECTACULAR_SETTINGS = {
    'TITLE': 'Graintrade Refactored API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}
