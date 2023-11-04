import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path)


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
# # public media settings
# PUBLIC_MEDIA_LOCATION = f"{AWS_STORAGE_BUCKET_NAME}/mediafiles"
# MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/"
# DEFAULT_FILE_STORAGE = "core.storage_backends.PublicMediaStorage"
# # private media settings
# PRIVATE_MEDIA_LOCATION = f"{AWS_STORAGE_BUCKET_NAME}/private"
# PRIVATE_FILE_STORAGE = "core.storage_backends.PrivateMediaStorage"

SPECTACULAR_SETTINGS = {
    'TITLE': 'Graintrade Refactored API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}
