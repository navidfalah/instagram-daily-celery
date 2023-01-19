from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
    
app.conf.beat_schedule = {
    
    'instagram-account-daily-update': {
        'task': 'update-accounts',  
        'schedule': crontab(hour=3, minute=30), 
    },
    'competitor-account-daily-update': {
        'task': 'update-competitors_account',      
        'schedule': crontab(hour=3, minute=30),
    },
    'update-posts_last-week': {
        'task': 'update-posts-week',     
        'schedule': crontab(hour=2, minute=30),
    },
    'update-competitor-posts-last-week': {
        'task': 'update-competitor-posts-week',    
        'schedule': crontab(hour=2, minute=30),
    },
} 