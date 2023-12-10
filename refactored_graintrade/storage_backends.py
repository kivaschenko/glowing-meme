# https://django-storages.readthedocs.io/en/latest/backends/azure.html

from django.conf import settings

from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = 'mediafiles'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = 'staticfiles'
    expiration_secs = None
