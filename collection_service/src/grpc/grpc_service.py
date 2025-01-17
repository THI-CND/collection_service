import grpc
from django_grpc_framework.services import Service
from ..models import Collection
from ..serializers import CollectionProtoSerializer, CollectionSerializer
from collection_service.src.grpc.stubs.collection_pb2 import ListCollectionResponse, DeleteCollectionResponse, ModifyRecipeResponse
from collection_service.src.rabbitmq.rabbitmq_sender import publish_event
import logging

logger = logging.getLogger(__name__)

class CollectionService(Service):
    def GetCollectionById(self, request, context):
        try:
            collection = Collection.objects.get(id=request.id)
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
            try:
                publish_event('collection_created', CollectionSerializer(collection).data)
            except Exception as e:
                logger.error(f"Failed to publish RabbitMQ event: {e}")

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
                try:
                    publish_event('collection_updated', CollectionSerializer(collection).data)
                except Exception as e:
                    logger.error(f"Failed to publish RabbitMQ event: {e}")

                return serializer.message
        except Collection.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Collection not found')
    
    def DeleteCollection(self, request, context):
        try:
            collection = Collection.objects.get(id=request.id)
            if collection.author != request.author:
                context.abort(grpc.StatusCode.PERMISSION_DENIED, 'Not authorized to delete this collection')
            # Trigger event
            try:
                publish_event('collection_deleted', CollectionSerializer(collection).data)
            except Exception as e:
                logger.error(f"Failed to publish RabbitMQ event: {e}")
                
            collection.delete()
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