# Updated master code with missing functions
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys

# Dictionary to store registered workers and their load
workers = {}

def register_worker(worker_name, worker_address):
    global workers
    workers[worker_name] = ServerProxy(worker_address)
    print(f"Worker {worker_name} registered at {worker_address}")

def get_worker():
    global workers
    # Balancing the load by selecting the worker with the least load
    return min(workers, key=lambda w: workers[w].get_load())

def getbyname(name):
    global workers
    worker_name = get_worker()
    try:
        return workers[worker_name].getbyname(name)
    except ConnectionRefusedError:
        return {'error': True, 'message': f'{worker_name} is unavailable'}

def getbylocation(location):
    global workers
    worker_name = get_worker()
    try:
        return workers[worker_name].getbylocation(location)
    except ConnectionRefusedError:
        return {'error': True, 'message': f'{worker_name} is unavailable'}

def getbyyear(location, year):
    global workers
    worker_name = get_worker()
    try:
        return workers[worker_name].getbyyear(location, year)
    except ConnectionRefusedError:
        return {'error': True, 'message': f'{worker_name} is unavailable'}

def main():
    port = int(sys.argv[1])
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    # Register RPC functions
    server.register_function(register_worker, 'register_worker')
    server.register_function(get_worker, 'get_worker')
    server.register_function(getbyname, 'getbyname')
    server.register_function(getbylocation, 'getbylocation')
    server.register_function(getbyyear, 'getbyyear')
    server.serve_forever()

if __name__ == '__main__':
    main()
