from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangorest.settings')

app = Celery('demo')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)