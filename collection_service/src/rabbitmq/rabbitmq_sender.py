import pika, json
from django.conf import settings
from .rabbitmq_config import connect, ensure_connection

def publish_event(event, message):
    channel = ensure_connection()  # Stelle sicher, dass die Verbindung und der Kanal offen sind
    properties = pika.BasicProperties(content_type='application/json', delivery_mode=2) # persistent messages
    
    try:
        channel.basic_publish(exchange=settings.RABBITMQ_EXCHANGE, routing_key=event, 
                            body=json.dumps(message), properties=properties)
        print(f"Message successfully published: {event}")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error sending message to {event}: {e}")
        connect()
        publish_event(event, message) 

def create_message(username, name, event):
    if event == 'collection.created':
        message = {#"id": 3, 
            "user": username,
            "title": "Collection created", 
            "message": f"Hello {username}, your new collection \"{name}\" was created."
        }
            
    elif event == 'collection.updated':
        message = {#"id": 3, 
                "user": username,
                "title": "Collection updated", 
                "message": f"Hello {username}, your collection \"{name}\" was updated."
        }
        
    elif event == 'collection.deleted':
        message = {#"id": 3, 
                "user": username,
                "title": "Collection deleted", 
                "message": f"Hello {username}, your collection \"{name}\" was deleted."
        }
    
    publish_event(event, message)

