import grpc
from .recipe_pb2 import RecipeIdRequest
from .recipe_pb2_grpc import RecipeServiceStub

class RecipeGrpcClient:
    def __init__(self, host='localhost', port=9098):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = RecipeServiceStub(self.channel)

    def get_recipe_tags(self, recipe_id):
        request = RecipeIdRequest(id=recipe_id)
        try:
            response = self.stub.GetAssociatedTags(request)
            print(response)
            return {
                "intersection": response.intersection,
                "union": response.union
            }
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            else:
                raise e