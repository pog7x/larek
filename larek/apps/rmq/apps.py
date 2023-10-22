import logging
import os
from threading import Thread

import pika
from django.apps import AppConfig

from larek.apps.rmq.consumer import RMQConsumer
from larek.apps.rmq.publisher import PublisherDlxQueue, RMQPublisher
from larek.apps.rmq.service import RMQService

logger = logging.getLogger(__name__)

RMQ_USER = os.getenv("RMQ_USER", "")
RMQ_PASSWORD = os.getenv("RMQ_PASSWORD", "")
RMQ_HOST = os.getenv("RMQ_HOST", "")
RMQ_PORT = os.getenv("RMQ_PORT", 5672)
RMQ_VHOST = os.getenv("RMQ_VHOST", "")

RMQ_PAYMENT_EXCHANGE = os.getenv("RMQ_PAYMENT_EXCHANGE", "")
RMQ_PAYMENT_QUEUE = os.getenv("RMQ_PAYMENT_QUEUE", "")
RMQ_PAYMENT_ROUTING_KEY = os.getenv("RMQ_PAYMENT_ROUTING_KEY", "")

RMQ_PAYMENT_DLX_EXCHANGE = os.getenv("RMQ_PAYMENT_DLX_EXCHANGE", "")
RMQ_PAYMENT_DLX_QUEUE = os.getenv("RMQ_PAYMENT_DLX_QUEUE", "")
RMQ_PAYMENT_DLX_ROUTING_KEY = os.getenv("RMQ_PAYMENT_DLX_ROUTING_KEY", "")

X_MESSAGE_TTL = 30 * 1000

larek_publisher = RMQPublisher(
    user=RMQ_USER,
    password=RMQ_PASSWORD,
    vhost=RMQ_VHOST,
    host=RMQ_HOST,
    port=RMQ_PORT,
    exchange_name=RMQ_PAYMENT_DLX_EXCHANGE,
    dlx_queue=PublisherDlxQueue(
        queue_name=RMQ_PAYMENT_DLX_QUEUE,
        arguments={
            "x-message-ttl": X_MESSAGE_TTL,
            "x-dead-letter-exchange": RMQ_PAYMENT_EXCHANGE,
            "x-dead-letter-routing-key": RMQ_PAYMENT_ROUTING_KEY,
        },
        routing_key=RMQ_PAYMENT_DLX_ROUTING_KEY,
    ),
)

larek_consumer = RMQConsumer(
    user=RMQ_USER,
    password=RMQ_PASSWORD,
    vhost=RMQ_VHOST,
    host=RMQ_HOST,
    port=RMQ_PORT,
    exchange_name=RMQ_PAYMENT_EXCHANGE,
    queue_name=RMQ_PAYMENT_QUEUE,
    routing_key=RMQ_PAYMENT_ROUTING_KEY,
    callback=RMQService.consume_payment_message,
)


class RmqConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "larek.apps.rmq"
    _connection, _channel = None, None
    CONSUMER_NAME = "Larek Payments Consumer"

    def ready(self):
        try:
            self._set_rmq()
            larek_publisher.connect()
            thr = Thread(
                name="mq_thread",
                daemon=True,
                target=larek_consumer.connect_and_start,
                kwargs={
                    "consume_params": {"consumer_tag": self.CONSUMER_NAME},
                },
            )
            thr.start()
        except Exception as err:
            logger.exception(f"RabbitmQ Config exception {err}")

    def _set_rmq(self):
        if not (self._connection and self._channel):
            credentials = pika.PlainCredentials(
                username=RMQ_USER,
                password=RMQ_PASSWORD,
            )
            conn_params = pika.ConnectionParameters(
                host=RMQ_HOST,
                port=RMQ_PORT,
                credentials=credentials,
            )

            if not self._connection:
                self._connection = pika.BlockingConnection(conn_params)
            if not self._channel:
                self._channel = self._connection.channel()

        self._channel.exchange_declare(
            exchange=RMQ_PAYMENT_EXCHANGE,
            durable=True,
        )
        larek_publisher._connection = self._connection
        larek_publisher._channel = self._channel

        larek_consumer._connection = self._connection
        larek_consumer._channel = self._channel
