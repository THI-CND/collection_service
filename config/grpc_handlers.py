import collection_service.src.grpc.collection_pb2_grpc as collection_pb2_grpc
from collection_service.src.grpc.grpc_service import CollectionService


def grpc_handlers(server):
    collection_pb2_grpc.add_CollectionServiceServicer_to_server(CollectionService.as_servicer(), server)