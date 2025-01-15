from rest_framework.views import APIView
from .rest_service import create_collection, update_collection, delete_collection, collection_add_recipe, collection_remove_recipe, collection_get_tags, get_collections, get_collection_by_id

class CollectionView(APIView):
    def get(self, request):
        return get_collections(request)

    def post(self, request):
        return create_collection(request)
    
class CollectionIDView(APIView):
    def get(self, request, id):
        return get_collection_by_id(request, id)

    def put(self, request, id):
        return update_collection(request, id)

    def delete(self, request, id):
        return delete_collection(request, id)

class CollectionRecipeView(APIView):
    def post(self, request, id):
        return collection_add_recipe(request, id)

    def delete(self, request, id):
        return collection_remove_recipe(request, id)
    
class CollectionTagView(APIView):
    def get(self, request, id):
        return collection_get_tags(request, id)
    
   