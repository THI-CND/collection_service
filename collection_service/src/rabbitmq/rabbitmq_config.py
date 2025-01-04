import pika
from django.conf import settings

credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
params = pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials)

# Globales connection und channel Objekt
connection = None
channel = None

# Funktion, um eine Verbindung und einen Kanal zu erstellen
def connect():
    global connection, channel
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange=settings.RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)
        
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
        
        # print("RabbitMQ connection and channel successfully created.")
    except pika.exceptions.AMQPConnectionError as e:
        print("Error while trying to connect to RabbitMQ:", e)
        raise

# Funktion zur Überprüfung der Verbindung und des Kanals
def ensure_connection():
    global connection, channel
    if connection is None or connection.is_closed:
        print("RabbitMQ connection is closed or not available. Reestablish connection...")
        connect()    
    return channel