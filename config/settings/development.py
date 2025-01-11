from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "collection-service"]

# Database
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("DB_NAME", default="collection"),
            'USER': env("DB_USER", default="postgres"),
            'PASSWORD': env("DB_PASSWORD", default="password"),
            'HOST': env("DB_HOST", default="postgres"),
            'PORT': env("DB_PORT", default=5432),
        }
    }

# RabbitMQ-Konfiguration
RABBITMQ_USER = env("RABBITMQ_USER", default="guest")
RABBITMQ_PASSWORD = env("RABBITMQ_PASSWORD", default="guest")
RABBITMQ_HOST = env("RABBITMQ_HOST", default="localhost")
RABBITMQ_PORT = env("RABBITMQ_PORT", default=5672)
RABBITMQ_EXCHANGE = env("RABBITMQ_EXCHANGE", default="recipemanagement")

routing_keys = env("RABBITMQ_ROUTING_KEYS_COLLECTION", default="collection.created,collection.updated,collection.deleted")
routing_keys_list = routing_keys.split(',')

RABBITMQ_ROUTING_KEYS = {
    'collection_created': routing_keys_list[0],
    'collection_updated': routing_keys_list[1],
    'collection_deleted': routing_keys_list[2],
}
