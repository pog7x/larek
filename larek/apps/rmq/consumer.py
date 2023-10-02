import logging

import pika

logger = logging.getLogger(__name__)


class RMQConsumer:
    _connect_retries = 20

    def __init__(
        self,
        user,
        password,
        vhost,
        host,
        port,
        exchange_name,
        queue_name,
        routing_key,
        callback,
        connection=None,
        channel=None,
    ) -> None:
        self._user = user
        self._password = password
        self._vhost = vhost
        self._host = host
        self._port = port
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._routing_key = routing_key
        self._callback = callback
        self._connection = connection
        self._channel = channel

    def _bind_queue(self):
        self._channel.queue_declare(queue=self._queue_name)
        self._channel.queue_bind(
            queue=self._queue_name,
            exchange=self._exchange_name,
            routing_key=self._routing_key,
        )

    def connect_and_start(self, consume_params={}):
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

        self._bind_queue()
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            queue=self._queue_name,
            on_message_callback=self._callback,
            **consume_params,
        )
        logger.info(f"Consumer [{self._queue_name}] start consuming...")
        self._channel.start_consuming()

    def _disconnect(self):
        if self._connection:
            self._connection.close()
        if self._channel:
            self._channel.stop_consuming()
            self._channel.close()
        self._connection, self._channel = None, None
