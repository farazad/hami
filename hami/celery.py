import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hami.settings')

app = Celery('hami')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() 