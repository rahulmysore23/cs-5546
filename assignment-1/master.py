from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys

# Dictionary to store registered workers and their load
workers = {"am": {}, "nz": {}}

def register_worker(worker_name, group, worker_address):
    global workers
    print(worker_name, group, worker_address)
    workers[group][worker_name] = ServerProxy(worker_address)
    print(f"Worker {worker_name} registered at {worker_address}")
    return {"message": "success"}

def get_worker(group):
    global workers
    # Balancing the load by selecting the worker with the least load
    option = min(workers[group], key=lambda w: workers[group][w].get_load())
    print("worker chose:", option)
    return workers[group][option]

def getbyname(name):
    global workers
    print("Get by name called:", name)
    
    first_letter = name[0].lower()
    if first_letter >= 'a' and first_letter <= 'm':
        # Call worker-1 for names starting with A-M
        worker = get_worker("am")
    elif first_letter >= 'n' and first_letter <= 'z':
        # Call worker-2 for names starting with N-Z
        worker = get_worker("nz")
    else:
        return {
            'error': True,
            'message': 'Invalid name'
        }
    try:
        return worker.getbyname(name)
    except ConnectionRefusedError:
        return {'error': True, 'message': f'{worker} is unavailable'}

def getbylocation(location):
    global workers
    print("Get by location called:", location)
    worker1 = get_worker("am")
    worker2 = get_worker("nz")
    try:
        result_1 = worker1.getbylocation(location)
    except ConnectionRefusedError:
        return {'error': True, 'message': f'{worker1} is unavailable'}
    try:
        result_2 = worker2.getbylocation(location)
    except ConnectionRefusedError:
        return {'error': True, 'message': f'{worker2} is unavailable'}
    return {"worker1_result": result_1, "worker2_result": result_2}

def getbyyear(location, year):
    global workers
    print("Get by year called:", year)
    worker1 = get_worker("am")
    worker2 = get_worker("nz")
    try:
        result_1 = worker1.getbyyear(location, year)
    except ConnectionRefusedError:
        return {'error': True, 'message': f'{worker1} is unavailable'}
    try:
        result_2 = worker2.getbyyear(location, year)
    except ConnectionRefusedError:
        return {'error': True, 'message': f'{worker2} is unavailable'}
    return {"worker1_result": result_1, "worker2_result": result_2}

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
