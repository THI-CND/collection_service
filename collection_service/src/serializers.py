from rest_framework import serializers
from django_grpc_framework import proto_serializers
from ..src.grpc import collection_pb2
from .models import Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'author', 'description', 'recipes']

class CollectionProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Collection
        proto_class = collection_pb2.CollectionResponse
        fields = ['id', 'name', 'author', 'description', 'recipes']