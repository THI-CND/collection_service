from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..models import Collection
from ..serializers import CollectionSerializer
from .rest_service import create_collection, update_collection, delete_collection, collection_add_recipe, collection_remove_recipe


class CollectionView(APIView):
    def get(self, request):
        collections = Collection.objects.all()
        if not collections:
            return Response(status=status.HTTP_204_NO_CONTENT)  # Keine Inhalte
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        return create_collection(request)
    

class CollectionIDView(APIView):
    def get(self, request, id):
        collection = Collection.objects.filter(pk=id).first()
        if not collection:
            return Response({"Collection": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

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
        collection = get_object_or_404(Collection, id=id)
        recipe_ids = collection.recipes
        #client = RecipeGrpcClient()
        #recipe_tags = client.get_recipe_tags(recipe_ids)
        recipe_tags = ["Food"]
        if not recipe_tags:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse(recipe_tags, safe=False, status=status.HTTP_200_OK)