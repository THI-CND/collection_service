from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..rabbitmq.rabbitmq_sender import create_message
from ..models import Collection
import json


def create_collection(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
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

    # Trigger event
    create_message(author, collection.name, 'collection.created')
    return JsonResponse({"id": collection.id}, status=201)


def delete_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    collection = get_object_or_404(Collection, id=id)
    #author = get_object_or_404(User, username=data['author']) 
    author = data['author']  
    if author != collection.author:
        return JsonResponse({"error": "Not authorized"}, status=403)
    
    # Trigger event
    create_message(author, collection.name, 'collection.deleted')
    collection.delete()
    return JsonResponse({"status": "deleted"}, status=200)


def update_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    required_fields = ["author", "name", "description"]
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required fields: : author, name, or description"}, status=400)
    
    collection = get_object_or_404(Collection, id=id)
    #author = get_object_or_404(User, username=data['author'])   
    author = data['author']
    if author != collection.author:
        return JsonResponse({"error": "Not authorized"}, status=403)
    
    collection.name = data['name']
    collection.description = data['description']
    collection.recipes.clear()

    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        #recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.append(recipe_id)
    
    collection.save()
    # Trigger event
    create_message(author, collection.name, 'collection.updated')
    return JsonResponse({"id": collection.id}, status=200)


def collection_add_recipe(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    recipe_id = data.get("recipe_id")
    if not recipe_id:
        return JsonResponse({"error": "Missing required field: recipe_id"}, status=400)
    
    collection = get_object_or_404(Collection, id=id)
    #recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe_id not in collection.recipes:
        collection.recipes.append(recipe_id)
        collection.save()
        return JsonResponse({"status": "added"}, status=200)
    else:
        return JsonResponse({"error": "Recipe already in collection"}, status=400)


def collection_remove_recipe(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    recipe_id = data.get("recipe_id")
    if not recipe_id:
        return JsonResponse({"error": "Missing required field: recipe_id"}, status=400)
    
    collection = get_object_or_404(Collection, id=id)
    #recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe_id in collection.recipes:
        collection.recipes.remove(recipe_id)
        collection.save()
        return JsonResponse({"status": "removed"}, status=200)
    else:
        return JsonResponse({"error": "Recipe not found in collection"}, status=404)
