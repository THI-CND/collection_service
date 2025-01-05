import pika, json
from pika.exceptions import AMQPConnectionError
from django.conf import settings
from .rabbitmq_config import rabbitmq_connection
import logging

logger = logging.getLogger(__name__)

def publish_event(event: str, payload: dict):
    """
    Publish an event to the RabbitMQ exchange.
    """
    try:
        # Establish or reuse the RabbitMQ connection and channel
        channel = rabbitmq_connection.ensure_connection()

        if channel is None:
            logger.warning("No RabbitMQ channel available. Skipping message publish.")
            return 
        
        # Serialize the message to JSON and set properties
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
        # Attempt reconnection and re-raise for the caller to handle
        rabbitmq_connection.connect()
        raise

    except Exception as e:
        logger.error("Unexpected error while publishing event: %s", str(e))
        raise

