import pika, json
from .rabbitmq_config import connect, ensure_connection

def publish_event(event, message):
        channel = ensure_connection()  # Stelle sicher, dass die Verbindung und der Kanal offen sind
        
        properties = pika.BasicProperties(content_type='application/json', delivery_mode=2) # persistent messages
        
        try:
                channel.basic_publish(exchange='collection_service_exchange', routing_key=event, 
                                body=json.dumps(message), properties=properties)
                print(f"Message successfully published: {event}")
    
        except pika.exceptions.AMQPConnectionError as e:
                print(f"Error sending message to {event}: {e}")
                # Versuche, die Verbindung und den Kanal erneut zu öffnen und Nachricht zu senden
                connect()
                publish_event(event, message) 


def create_message(user, name, event):
    user_name = user.username
    if event == 'collection.created':
        message = {#"id": 3, 
            "user": user_name, #hier irgendwann der eingeloggte User
            "title": 'Collection created', 
            "message": f'Hello {user_name}, your new collection "{name}" was created.'
        }
            
    elif event == 'collection.updated':
        message = {#"id": 3, 
                "user": user_name, #hier irgendwann der eingeloggte User
                "title": 'Collection updated', 
                "message": f'Hello {user_name}, your collection "{name}" was updated.'
        }
        
    elif event == 'collection.deleted':
        message = {#"id": 3, 
                "user": user_name, #hier irgendwann der eingeloggte User
                "title": 'Collection deleted', 
                "message": f'Hello {user_name}, your collection "{name}" was deleted.'
        }
    
    publish_event(event, message)

