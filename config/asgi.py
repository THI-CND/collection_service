# Zweck: Konfiguration für ASGI (Asynchronous Server Gateway Interface) für Django-App
# für Produktionsumgebungen; Stellt Schnittstelle von fortgeschrittenen/modernen Web-Servern zu Django-App her (asynchroner Code)

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")


application = get_asgi_application()