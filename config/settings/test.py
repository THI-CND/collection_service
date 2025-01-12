from .base import *

DEBUG = False

#Database
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "test_db.sqlite3",
        }
    }

# RabbitMQ-Konfiguration
RABBITMQ_USER = "test"
RABBITMQ_PASSWORD = "test"
RABBITMQ_HOST = "test"
RABBITMQ_PORT = 1234
RABBITMQ_EXCHANGE = "test"