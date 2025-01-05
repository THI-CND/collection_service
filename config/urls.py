"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import collection_service.src.grpc.collection_pb2_grpc as collection_pb2_grpc
from collection_service.src.grpc.grpc_service import CollectionService

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("collection_service.src.rest.urls"))
]

def grpc_handlers(server):
    collection_pb2_grpc.add_CollectionServiceServicer_to_server(CollectionService.as_servicer(), server)