from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from .rabbitmq.rabbitmq_sender import create_message
from .models import Collection, Recipe, User
import json

# Create your views here.

invalid_json = "Invalid JSON"

def get_collection(id):
    collection = get_object_or_404(Collection, id=id)
    return JsonResponse(collection_to_dict(collection))


def get_collections():
    collections = Collection.objects.all()
    if not collections:
        return HttpResponse(status=204)  # Keine Inhalte
    return JsonResponse([collection_to_dict(c) for c in collections], safe=False, status=200)


def create_collection(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
    if 'author' not in data or 'name' not in data or 'description' not in data:
        return HttpResponseBadRequest("Missing required fields: author, name, or description")

    author = get_object_or_404(User, username=data['author'])
    
    collection = Collection.objects.create(
        name=data['name'],
        author=author,
        description=data['description']
    )
    
    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.add(recipe)

    # Trigger event
    create_message(author, collection.name, 'collection.created')
    return JsonResponse(collection_to_dict(collection), status=201)


def delete_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
    collection = get_object_or_404(Collection, id=id)
    author = get_object_or_404(User, username=data['author'])   
    if author != collection.author:
        return HttpResponseForbidden("You are not authorized to delete this collection")
    
    # Trigger event
    create_message(author, collection.name, 'collection.deleted')
    collection.delete()
    return JsonResponse({'status': 'deleted'}, status=200)


def update_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
    if 'author' not in data or 'name' not in data or 'description' not in data:
        return HttpResponseBadRequest("Missing required fields: author, name, or description")
    
    collection = get_object_or_404(Collection, id=id)
    author = get_object_or_404(User, username=data['author'])   
    if author != collection.author:
        return HttpResponseForbidden("You are not authorized to update this collection")
    
    collection.name = data['name']
    collection.description = data['description']
    collection.recipes.clear()

    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.add(recipe)
    
    collection.save()
    # Trigger event
    create_message(author, collection.name, 'collection.updated')
    return JsonResponse(collection_to_dict(collection), status=200)


def collection_add_recipe(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
    if 'recipe_id' not in data:
        return HttpResponseBadRequest("Missing required field: recipe_id")
    
    recipe_id = data.get('recipe_id')
    collection = get_object_or_404(Collection, id=id)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    collection.recipes.add(recipe)
    
    return JsonResponse(collection_to_dict(collection), status=200)


def collection_remove_recipe(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
    if 'recipe_id' not in data:
        return HttpResponseBadRequest("Missing required field: recipe_id")
    
    recipe_id = data.get('recipe_id')
    collection = get_object_or_404(Collection, id=id)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    collection.recipes.remove(recipe)
    return JsonResponse(collection_to_dict(collection), status=200)


def collection_to_dict(collection):
    return {
        'id': collection.id,
        'name': collection.name,
        'author': collection.author.username,
        'description': collection.description,
        'recipes': [recipe.id for recipe in collection.recipes.all()]
    }