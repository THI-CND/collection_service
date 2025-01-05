import pika
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class RabbitMQConnection:
    def __init__(self):
        self._connection = None
        self._channel = None
        self._params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASSWORD
            ),
            heartbeat=60,
            blocked_connection_timeout=30,
        )

    def connect(self):
        """Establish the RabbitMQ connection and channel."""
        try:
            self._connection = pika.BlockingConnection(self._params)
            self._channel = self._connection.channel()
            self._channel.exchange_declare(
                exchange=settings.RABBITMQ_EXCHANGE,
                exchange_type='topic',
                durable=True,
            )

            # Nur zum Debuggen
        # channel.queue_declare(queue='collection.created', durable=True)
        # channel.queue_declare(queue='collection.updated', durable=True)
        # channel.queue_declare(queue='collection.deleted', durable=True)
        
        # exchange = 'collection_service_exchange'
        # channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
        
        # # Nur zum Debuggen
        # channel.queue_bind(exchange=exchange, queue='collection.created', routing_key='collection.created.#')
        # channel.queue_bind(exchange=exchange, queue='collection.updated', routing_key='collection.updated.#')
        # channel.queue_bind(exchange=exchange, queue='collection.deleted', routing_key='collection.deleted.#')


            logger.info("RabbitMQ connection and channel successfully established.")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("Failed to connect to RabbitMQ: %s. Continuing without RabbitMQ.", str(e))
            self._connection = None
            self._channel = None
        except Exception as e:
            logger.error("Unexpected error while connecting to RabbitMQ: %s", str(e))
            self._connection = None
            self._channel = None
        
    def ensure_connection(self):
        """Ensure the connection and channel are open."""
        if self._connection is None or self._connection.is_closed:
            if self._connection is None:
                logger.info("No RabbitMQ connection found. Establishing the first connection...")
            else:
                logger.warning("RabbitMQ connection is closed. Reconnecting...")
            self.connect()

        if self._channel is None:
            logger.warning("RabbitMQ channel could not be established.")
        return self._channel
    
    def close(self):
        """Close the RabbitMQ connection."""
        if self._connection and self._connection.is_open:
            self._connection.close()
            logger.info("RabbitMQ connection closed.")

rabbitmq_connection = RabbitMQConnection()

