import pika, json
from pika.exceptions import AMQPConnectionError
from django.conf import settings
from .rabbitmq_config import rabbitmq_connection
import logging

logger = logging.getLogger(__name__)

def publish_event(event: str, payload: dict, connection=None):
    if connection is None:
        connection = rabbitmq_connection
    channel = connection.ensure_connection()
    properties = pika.BasicProperties(
        content_type='application/json',
        delivery_mode=2,
    )
    channel.basic_publish(
        exchange=settings.RABBITMQ_EXCHANGE,
        routing_key=settings.RABBITMQ_ROUTING_KEYS[event],
        body=json.dumps(payload),
        properties=properties
    )