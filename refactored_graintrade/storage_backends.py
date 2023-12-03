# https://django-storages.readthedocs.io/en/latest/backends/azure.html

from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = 'csb100320031c4ce7be'  # Must be replaced by your <storage_account_name>
    account_key = 'AilnMKnrpcnkycx9wnqxCr+3ghYGoMyyOf4xQjgx1o9DBTHi3LNkuVbuhU0awlEaYVFNDdQdywqx+AStlKWdMQ=='  # Must be replaced by your <storage_account_key>
    azure_container = 'mediafiles'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = 'csb100320031c4ce7be' # Must be replaced by your storage_account_name
    account_key = 'AilnMKnrpcnkycx9wnqxCr+3ghYGoMyyOf4xQjgx1o9DBTHi3LNkuVbuhU0awlEaYVFNDdQdywqx+AStlKWdMQ=='  # Must be replaced by your <storage_account_key>
    # account_key = 'SY79B9ANkWCBLBKSR4TAU+bru+hTRlz8Z8y+tKfgXuqshGjyICNgTW5X7X8b/QAE3bHvtk84Zy+t+ASt2MjVOQ=='  # Must be replaced by your <storage_account_key>
    azure_container = 'staticfiles'
    expiration_secs = None
