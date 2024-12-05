from rest_framework import serializers
from .models import Collection

class CollectionSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'author', 'description', 'recipes']