import grpc
from django_grpc_framework.services import Service
from ..models import Collection
from ..serializers import CollectionProtoSerializer
from collection_service.src.grpc.collection_pb2 import ListCollectionResponse, DeleteCollectionResponse, ModifyRecipeResponse
from collection_service.src.rabbitmq.rabbitmq_sender import create_message


class CollectionService(Service):
    def GetCollectionById(self, request, context):
        try:
            collection = Collection.objects.get(id=request.id)
            print(CollectionProtoSerializer(collection).message)
            return CollectionProtoSerializer(collection).message
        except Collection.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Collection not found')
    
    def GetCollections(self, request, context):
        collections = Collection.objects.all()
        serializer = CollectionProtoSerializer(collections, many=True)
        return ListCollectionResponse(collections=serializer.message)
    
    def CreateCollection(self, request, context):
        serializer = CollectionProtoSerializer(data={
            'name': request.name,
            'author': request.author,
            'description': request.description,
            'recipes': list(request.recipes)
        })
        if serializer.is_valid(raise_exception=True):
            collection = serializer.save()
            # Trigger event
            create_message(collection.author, collection.name, 'collection.created')
            return serializer.message
        
    def UpdateCollection(self, request, context):
        try:
            collection = Collection.objects.get(id=request.id)
            if collection.author != request.author:
                context.abort(grpc.StatusCode.PERMISSION_DENIED, 'Not authorized to delete this collection')
            serializer = CollectionProtoSerializer(collection, data={
                'name': request.name,
                'author': request.author,
                'description': request.description,
                'recipes': list(request.recipes)
            })
            if serializer.is_valid(raise_exception=True):
                collection = serializer.save()
                # Trigger event
                print(collection.author, collection.name)
                create_message(collection.author, collection.name, 'collection.updated')
                return serializer.message
        except Collection.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Collection not found')
    
    def DeleteCollection(self, request, context):
        try:
            collection = Collection.objects.get(id=request.id)
            if collection.author != request.author:
                context.abort(grpc.StatusCode.PERMISSION_DENIED, 'Not authorized to delete this collection')
            collection.delete()
            # Trigger event
            create_message(collection.author, collection.name, 'collection.deleted')
            return DeleteCollectionResponse(status="Collection deleted")
        except Collection.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Collection not found')
    
    def AddRecipeToCollection(self, request, context):
        try:
            collection = Collection.objects.get(id=request.id)
            if request.recipe_id not in collection.recipes:
                collection.recipes.append(request.recipe_id)
                collection.save()
                return ModifyRecipeResponse(status="Recipe added")
            else:
                context.abort(grpc.StatusCode.ALREADY_EXISTS, 'Recipe already in collection')
        except Collection.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Collection not found')
          
    def RemoveRecipeFromCollection(self, request, context):
        try:
            collection = Collection.objects.get(id=request.id)
            if request.recipe_id in collection.recipes:
                collection.recipes.remove(request.recipe_id)
                collection.save()
                return ModifyRecipeResponse(status="Recipe removed")
            else:
                context.abort(grpc.StatusCode.NOT_FOUND, 'Recipe not found in collection')
        except Collection.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Collection not found')