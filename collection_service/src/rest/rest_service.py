from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from ..rabbitmq.rabbitmq_sender import publish_event
from ..models import Collection
from ..serializers import CollectionSerializer
from ..grpc.grpc_recipe_client import RecipeGrpcClient
import json
import logging

logger = logging.getLogger(__name__)

def create_collection(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    required_fields = ["author", "name", "description"]
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required fields: : author, name, or description"}, status=status.HTTP_400_BAD_REQUEST)

    author = data['author']
    
    collection = Collection.objects.create(
        name=data['name'],
        author=author,
        description=data['description']
    )
    
    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        collection.recipes.append(recipe_id)
    
    collection.save()
    # Trigger event
    try:
        collection_data = CollectionSerializer(collection).data
        publish_event('collection_created', collection_data)
    except Exception as e:
        logger.error(f"Failed to publish RabbitMQ event: {e}")

    return JsonResponse({"id": collection.id}, status=status.HTTP_201_CREATED)


def delete_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    collection = get_object_or_404(Collection, id=id)
    author = data['author']  
    if author != collection.author:
        return JsonResponse({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    # Trigger event
    try:
        collection_data = CollectionSerializer(collection).data
        publish_event('collection_deleted', collection_data)
    except Exception as e:
        logger.error(f"Failed to publish RabbitMQ event: {e}")

    collection.delete()
    return JsonResponse({"status": "deleted"}, status=status.HTTP_200_OK)


def update_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    required_fields = ["author", "name", "description"]
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required fields: : author, name, or description"}, status=status.HTTP_400_BAD_REQUEST)
    
    collection = get_object_or_404(Collection, id=id)
    author = data['author']
    if author != collection.author:
        return JsonResponse({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    collection.name = data['name']
    collection.description = data['description']
    collection.recipes.clear()

    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        collection.recipes.append(recipe_id)
    
    collection.save()
    # Trigger event
    try:
        collection_data = CollectionSerializer(collection).data
        publish_event('collection_updated', collection_data)
    except Exception as e:
        logger.error(f"Failed to publish RabbitMQ event: {e}")
        
    return JsonResponse({"id": collection.id}, status=status.HTTP_200_OK)


def collection_add_recipe(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    recipe_id = data.get("recipe_id")
    if not recipe_id:
        return JsonResponse({"error": "Missing required field: recipe_id"}, status=status.HTTP_400_BAD_REQUEST)
    
    collection = get_object_or_404(Collection, id=id)
    if recipe_id not in collection.recipes:
        collection.recipes.append(recipe_id)
        collection.save()
        return JsonResponse({"status": "added"}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Recipe already in collection"}, status=status.HTTP_409_CONFLICT)


def collection_remove_recipe(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    recipe_id = data.get("recipe_id")
    if not recipe_id:
        return JsonResponse({"error": "Missing required field: recipe_id"}, status=status.HTTP_400_BAD_REQUEST)
    
    collection = get_object_or_404(Collection, id=id)
    if recipe_id in collection.recipes:
        collection.recipes.remove(recipe_id)
        collection.save()
        return JsonResponse({"status": "removed"}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Recipe not found in collection"}, status=status.HTTP_404_NOT_FOUND)
    

def collection_get_tags(request, id):
    collection = get_object_or_404(Collection, id=id)

    if not collection.recipes:
        return JsonResponse({"detail": "No recipes in the collection"}, status=status.HTTP_204_NO_CONTENT)
    
    client = RecipeGrpcClient()
    all_tags = []
    intersection_tags = []
    
    for recipe_id in collection.recipes:
        tags = client.get_recipe_tags(recipe_id)
        if not tags:
            continue
        all_tags.append(tags['union'])
        if intersection_tags == []:
            intersection_tags = set(tags['intersection'])
        else:
            intersection_tags &= set(tags['intersection'])

    union_tags = set().union(*all_tags)

    result = {
        "intersection": list(intersection_tags),
        "union": list(union_tags)
    }
    if not result:
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
