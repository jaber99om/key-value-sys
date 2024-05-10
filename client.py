import grpc
import kvstore_pb2 # type: ignore
import kvstore_pb2_grpc # type: ignore

def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Put(kvstore_pb2.PutRequest(key='hello', value='world'))
        print("Put Response: ", response.success)
        
        response = stub.Get(kvstore_pb2.GetRequest(key='hello'))
        if response.found:
            print("Get Response: ", response.value)
        else:
            print("Key not found")
        
        response = stub.Delete(kvstore_pb2.DeleteRequest(key='hello'))
        print("Delete Response: ", response.success)

if __name__ == '__main__':
    run_client()
