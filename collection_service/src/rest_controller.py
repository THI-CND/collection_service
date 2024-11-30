from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .views import get_collections, get_collection, create_collection, update_collection, delete_collection, collection_add_recipe, collection_remove_recipe

invalid_request = "Invalid request method"

@csrf_exempt #CSRF-Token Überprüfung wird deaktiviert
def collection_main(request):
    if request.method == 'GET':
        return get_collections()
    elif request.method == 'POST':
        return create_collection(request)
    else:
        return HttpResponseBadRequest(invalid_request)

@csrf_exempt #CSRF-Token Überprüfung wird deaktiviert
def collection_main_id(request, id=None):
    if request.method == 'GET':
        return get_collection(id)
    elif request.method == 'PUT':
        return update_collection(request, id)
    elif request.method == 'DELETE':
        return delete_collection(request, id)
    else:
        return HttpResponseBadRequest(invalid_request)
 

@csrf_exempt #CSRF-Token Überprüfung wird deaktiviert
def collection_edit_recipe(request, id):
    if request.method == 'POST':
        return collection_add_recipe(request, id)
    elif request.method == 'DELETE':
        return collection_remove_recipe(request, id)
    else:
        return HttpResponseBadRequest(invalid_request)