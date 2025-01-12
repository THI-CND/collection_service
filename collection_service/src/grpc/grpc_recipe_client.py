import grpc
from .recipe_pb2 import RecipeIdRequest
from .recipe_pb2_grpc import RecipeServiceStub
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class RecipeGrpcClient:
    def __init__(self):
        host = settings.GRPC_HOST_RECIPE_SERVICE
        port = settings.GRPC_PORT_RECIPE_SERVICE
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = RecipeServiceStub(self.channel)

    def get_recipe_tags(self, recipe_id):
        request = RecipeIdRequest(id=recipe_id)
        try:
            response = self.stub.GetAssociatedTags(request)
            return {
                "intersection": response.intersection,
                "union": response.union
            }
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                logger.error("Recipe gRPC server is unavailable. Please check the server status.")
                raise e
            else:
                raise e