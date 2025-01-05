from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from ..rabbitmq.rabbitmq_sender import publish_event
from ..models import Collection
from ..serializers import CollectionSerializer
import json


def create_collection(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    required_fields = ["author", "name", "description"]
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required fields: : author, name, or description"}, status=400)

    #author = get_object_or_404(User, username=data['author'])
    author = data['author']
    
    collection = Collection.objects.create(
        name=data['name'],
        author=author,
        description=data['description']
    )
    
    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        #recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.append(recipe_id)
    
    collection.save()
    # Trigger event
    collection_data = CollectionSerializer(collection).data
    publish_event('collection_created', collection_data)
    return JsonResponse({"id": collection.id}, status=status.HTTP_201_CREATED)


def delete_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    collection = get_object_or_404(Collection, id=id)
    #author = get_object_or_404(User, username=data['author']) 
    author = data['author']  
    if author != collection.author:
        return JsonResponse({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    # Trigger event
    collection_data = CollectionSerializer(collection).data
    publish_event('collection_deleted', collection_data)
    collection.delete()
    return JsonResponse({"status": "deleted"}, status=status.HTTP_200_OK)


def update_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    required_fields = ["author", "name", "description"]
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required fields: : author, name, or description"}, status=400)
    
    collection = get_object_or_404(Collection, id=id)
    #author = get_object_or_404(User, username=data['author'])   
    author = data['author']
    if author != collection.author:
        return JsonResponse({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    collection.name = data['name']
    collection.description = data['description']
    collection.recipes.clear()

    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        #recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.append(recipe_id)
    
    collection.save()
    # Trigger event
    collection_data = CollectionSerializer(collection).data
    publish_event('collection_updated', collection_data)
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
    #recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe_id not in collection.recipes:
        collection.recipes.append(recipe_id)
        collection.save()
        return JsonResponse({"status": "added"}, status=200)
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
    #recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe_id in collection.recipes:
        collection.recipes.remove(recipe_id)
        collection.save()
        return JsonResponse({"status": "removed"}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Recipe not found in collection"}, status=status.HTTP_404_NOT_FOUND)
