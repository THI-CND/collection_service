from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]

# Database
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"),
            'PASSWORD': env("DB_PASSWORD"),
            'HOST': env("DB_HOST"),
            'PORT': env("DB_PORT"),
        }
    }

# RabbitMQ-Configuration
RABBITMQ_USER = env("RABBITMQ_USER")
RABBITMQ_PASSWORD = env("RABBITMQ_PASSWORD")
RABBITMQ_HOST = env("RABBITMQ_HOST")
RABBITMQ_PORT = env("RABBITMQ_PORT")
RABBITMQ_EXCHANGE = env("RABBITMQ_EXCHANGE")

routing_keys = env("RABBITMQ_ROUTING_KEYS_COLLECTION")
routing_keys_list = routing_keys.split(',')

RABBITMQ_ROUTING_KEYS = {
    'collection_created': routing_keys_list[0],
    'collection_updated': routing_keys_list[1],
    'collection_deleted': routing_keys_list[2],
}

# GRPC-Configuration Recipe-Service
GRPC_HOST_RECIPE_SERVICE = env("GRPC_HOST_RECIPE_SERVICE")
GRPC_PORT_RECIPE_SERVICE = env("GRPC_PORT_RECIPE_SERVICE")