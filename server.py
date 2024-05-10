import grpc
from concurrent import futures
import kvstore_pb2 # type: ignore
import kvstore_pb2_grpc # type: ignore

class KeyValueStoreServicer(kvstore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        # initialize your database or any state
        self.store = {}

    def Put(self, request, context):
        self.store[request.key] = request.value
        return kvstore_pb2.PutResponse(success=True)

    def Get(self, request, context):
        value = self.store.get(request.key, None)
        found = value is not None
        return kvstore_pb2.GetResponse(value=value or "", found=found)

    def Delete(self, request, context):
        if request.key in self.store:
            del self.store[request.key]
            return kvstore_pb2.DeleteResponse(success=True)
        return kvstore_pb2.DeleteResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
