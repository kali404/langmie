from celery import Celery
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "boxuegu.settings"

celery_app = Celery()
celery_app.config_from_object('celery_tasks.config')
# 自动识别

celery_app.autodiscover_tasks([
    'celery_tasks.mail',
])

