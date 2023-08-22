from __future__ import absolute_import

import os

import configurations
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'refactored_graintrade.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')

configurations.setup()

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('request: {0!r}'.format(self.request))