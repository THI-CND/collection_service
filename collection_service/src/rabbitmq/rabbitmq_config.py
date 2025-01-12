import pika
from pika.exceptions import AMQPConnectionError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class RabbitMQConnection:
    def __init__(self, host, port, user, password, exchange):
        self._params = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(user, password)
        )
        self._exchange = exchange
        self._connection = None
        self._channel = None

    def ensure_connection(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = pika.BlockingConnection(self._params)
            self._channel = self._connection.channel()
            self._channel.exchange_declare(
                exchange=self._exchange,
                exchange_type='topic',
                durable=True
            )
        return self._channel

    def close(self):
        if self._connection and self._connection.is_open:
            self._connection.close()

rabbitmq_connection = RabbitMQConnection(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    user=settings.RABBITMQ_USER,
    password=settings.RABBITMQ_PASSWORD,
    exchange=settings.RABBITMQ_EXCHANGE
)
