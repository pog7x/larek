import json
import logging
from dataclasses import dataclass

import pika

logger = logging.getLogger(__name__)


@dataclass
class PublisherDlxQueue:
    queue_name: str
    arguments: dict
    routing_key: str


class RMQPublisher:
    _publish_retries = 20

    def __init__(
        self,
        user,
        password,
        vhost,
        host,
        port,
        exchange_name,
        connection=None,
        channel=None,
        dlx_queue: PublisherDlxQueue = None,
    ) -> None:
        self._user = user
        self._password = password
        self._vhost = vhost
        self._host = host
        self._port = port
        self._exchange_name = exchange_name
        self._connection = connection
        self._channel = channel
        self._dlx_queue = dlx_queue

    def connect(self):
        if not (self._connection and self._channel):
            credentials = pika.PlainCredentials(
                username=self._user,
                password=self._password,
            )
            conn_params = pika.ConnectionParameters(
                host=self._host,
                port=self._port,
                credentials=credentials,
            )

            if not self._connection:
                self._connection = pika.BlockingConnection(conn_params)
            if not self._channel:
                self._channel = self._connection.channel()

        self._channel.basic_qos(prefetch_count=1)
        self._declare_exchange()

        if self._dlx_queue:
            self._bind_dlx_queue()
        logger.info(f"Publisher [{self._exchange_name}] connected!")

    def _publish(self, message, routing_key):
        self._channel.basic_publish(
            exchange=self._exchange_name,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def _declare_exchange(self):
        self._channel.exchange_declare(
            exchange=self._exchange_name,
            durable=True,
        )

    def _bind_dlx_queue(self):
        self._channel.queue_declare(
            queue=self._dlx_queue.queue_name,
            arguments=self._dlx_queue.arguments,
        )
        self._channel.queue_bind(
            queue=self._dlx_queue.queue_name,
            exchange=self._exchange_name,
            routing_key=self._dlx_queue.routing_key,
        )
        logger.info(f"Publisher DLX Queue [{self._dlx_queue.queue_name}] bound!")

    def publish(self, data, routing_key=None):
        msg = json.dumps(data)

        if not routing_key:
            routing_key = (
                self._dlx_queue.routing_key
                if self._dlx_queue and self._dlx_queue.routing_key
                else ""
            )

        for _ in range(self._publish_retries):
            try:
                self._publish(message=msg, routing_key=routing_key)
                return
            except Exception:
                self._disconnect()
                self.connect()
                continue

        raise Exception(f"RMQPublisher: message {data} not published.")

    def _disconnect(self):
        if self._connection and not self._connection.is_closed:
            self._connection.close()
        if self._channel and not self._channel.is_closed:
            self._channel.close()
        self._connection, self._channel = None, None
