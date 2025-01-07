import pika, json
from pika.exceptions import AMQPConnectionError
from django.conf import settings
from .rabbitmq_config import rabbitmq_connection
import logging

logger = logging.getLogger(__name__)

def publish_event(event: str, payload: dict, retry_count=2):
    """
    Publish an event to the RabbitMQ exchange.
    """
    try:
        channel = rabbitmq_connection.ensure_connection()
        # Serialize the message to JSON and set properties

        if channel is None:
            logger.warning("No RabbitMQ channel available. Skipping message publish.")
            return
        
        properties = pika.BasicProperties(
            content_type='application/json',
            delivery_mode=2,  # Persistent messages
        )
        message_json = json.dumps(payload)

        # Publish the message
        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=settings.RABBITMQ_ROUTING_KEYS[event],
            body=message_json,
            properties=properties,
        )
        logger.info("Message successfully published: event=%s, message=%s", event, payload)

    except AMQPConnectionError as e:
        logger.error("Failed to send message to RabbitMQ: %s", str(e))
        if retry_count > 0:
            logger.info("Retrying... Remaining attempts: %d", retry_count)
            rabbitmq_connection.connect()
            publish_event(event, payload, retry_count=retry_count - 1)
        else:
            logger.error("Max retry attempts reached. Giving up on publishing the message.")

