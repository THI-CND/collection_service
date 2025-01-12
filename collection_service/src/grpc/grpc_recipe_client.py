import grpc
from .recipe_pb2 import RecipeIdRequest
from .recipe_pb2_grpc import RecipeServiceStub


def get_associated_tags(recipe_id: str):
    channel = grpc.insecure_channel('recipe_service:9098')
    stub = RecipeServiceStub(channel)

    # Erstelle die Anfrage
    request = RecipeIdRequest(id=recipe_id)

    # Rufe die Methode GetAssociatedTags auf
    response = stub.GetAssociatedTags(request)

    # Verarbeite die Antwort
    print("Intersection:", response.intersection)
    print("Union:", response.union)

class RecipeGrpcClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = RecipeServiceStub(self.channel)

    def get_recipe_tags(self, recipe_id):
        request = RecipeIdRequest(id=recipe_id)
        response = self.stub.GetAssociatedTags(request)
        print("Intersection:", response.intersection)
        print("Union:", response.union)

        return response.tags