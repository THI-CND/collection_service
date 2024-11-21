import pika, json
import os

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')
rabbitmq_host = os.getenv('RABBITMQ_HOST')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
params = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials, heartbeat=120)

connection = pika.BlockingConnection(params)
#params = pika.URLParameters('amqp://guest:guest@localhost:5672/')
#connection = pika.BlockingConnection(params)


exchange = 'collection_service_exchange'
channel = connection.channel()

#Nur zum Debuggen
channel.queue_declare(queue='collection.created', durable=True)
channel.queue_declare(queue='collection.updated', durable=True)
channel.queue_declare(queue='collection.deleted', durable=True)

channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)

#Nur zum Debuggen
channel.queue_bind(exchange=exchange,queue='collection.created',routing_key='collection.created')
channel.queue_bind(exchange=exchange,queue='collection.updated',routing_key='collection.updated')
channel.queue_bind(exchange=exchange,queue='collection.deleted',routing_key='collection.deleted')

def publishEvent(method, body):
        if connection.is_open:
                if not hasattr(connection, 'channel') or not connection.channel.is_open:
                        channel = connection.channel()

        body = {#"id": 3, 
                "user": "Testuser", #hier irgendwann der eingeloggte User
                "title": "Testtitel", 
                "message": "Dies ist eine Testnachricht. Blub"}
        channel.basic_publish(exchange=exchange, routing_key=method, body=json.dumps(body))