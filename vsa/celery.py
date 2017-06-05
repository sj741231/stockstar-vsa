# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vsa.settings')

from django.conf import settings

app = Celery('vsa')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#crontab config
app.conf.update(
    CELERYBEAT_SCHEDULE = {
        # Executes every Monday morning at 7:30 A.M
        'every-60-min-update-job-status': {
            'task': 'collect_ip_mac',
            'schedule': timedelta(seconds=1800),
            'args': (300,),
        }
    }
)






@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))