import pika, json
import os

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')
rabbitmq_host = os.getenv('RABBITMQ_HOST')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
params = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

#params = pika.URLParameters('amqp://guest:guest@localhost:5672/')
#connection = pika.BlockingConnection(params)

# Globales connection und channel Objekt
connection = None
channel = None

# Funktion, um eine Verbindung und einen Kanal zu erstellen
def connect():
    global connection, channel
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        # Nur zum Debuggen
        channel.queue_declare(queue='collection.created', durable=True)
        channel.queue_declare(queue='collection.updated', durable=True)
        channel.queue_declare(queue='collection.deleted', durable=True)
        
        exchange = 'collection_service_exchange'
        channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
        
        # Nur zum Debuggen
        channel.queue_bind(exchange=exchange, queue='collection.created', routing_key='collection.created')
        channel.queue_bind(exchange=exchange, queue='collection.updated', routing_key='collection.updated')
        channel.queue_bind(exchange=exchange, queue='collection.deleted', routing_key='collection.deleted')
        
        print("RabbitMQ connection and channel successfully created.")
    
    except pika.exceptions.AMQPConnectionError as e:
        print("Error while trying to connect to RabbitMQ:", e)
        raise

# Funktion zur Überprüfung der Verbindung und des Kanals
def ensure_connection():
    global connection, channel
    if connection is None or connection.is_closed:
        print("RabbitMQ connection is closed or not available. Reestablish connection...")
        connect()
    elif not channel.is_open:
        print("RabbitMQ channel is closed. Open new channel...")
        channel = connection.channel()

def publish_event(method, body):
        ensure_connection()  # Stelle sicher, dass die Verbindung und der Kanal offen sind
                
        body = {#"id": 3, 
                "user": "Testuser", #hier irgendwann der eingeloggte User
                "title": "Testtitel", 
                "message": "Dies ist eine Testnachricht. Blub"}
        properties = pika.BasicProperties(content_type='application/json', delivery_mode=2) # persistent messages
        
        try:
                channel.basic_publish(exchange='collection_service_exchange', routing_key=method, 
                                body=json.dumps(body), properties=properties)
                print(f"Message successfully published: {method}")
    
        except pika.exceptions.AMQPConnectionError as e:
                print(f"Error sending message to {method}: {e}")
                # Versuche, die Verbindung und den Kanal erneut zu öffnen und Nachricht zu senden
                connect()
                publish_event(method, body) 