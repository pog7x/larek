import os

from celery import Celery
from kombu import Queue

BROKER_URL = os.getenv("RMQ_URL", "")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "larek.settings")

CELERY_BROKER_URL = BROKER_URL

app = Celery("larek")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.broker_url = BROKER_URL
app.conf.task_default_queue = "larek"
app.conf.task_queues = (Queue("larek", routing_key="task.#"),)
app.conf.task_default_exchange = "larek"
app.conf.task_default_exchange_type = "topic"
app.conf.task_default_routing_key = "task.larek"
