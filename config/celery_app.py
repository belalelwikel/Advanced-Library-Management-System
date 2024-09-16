import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")



from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from pathlib import Path
import environ
from datetime import timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery("lms")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



