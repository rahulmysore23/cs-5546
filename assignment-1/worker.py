# Updated worker code with registration logic
from xmlrpc.server import SimpleXMLRPCServer
import sys
import json
import xmlrpc.client

# Storage of data
data_table = {}
requests_served = 0

# Function to load data from a JSON file based on group
def load_data(group):
    global data_table
    filename = f"data-{group}.json"
    print(f"Filename: '{filename}'")
    try:
        with open(filename, 'r') as file:
            data_table = json.load(file)
        print(f"Data loaded successfully for group {group}.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from file '{filename}'.")

# Function to register the worker with the master server
def register_with_master(master_port, worker_name, worker_port, group):
    try:
        with xmlrpc.client.ServerProxy(f"http://localhost:{master_port}/") as master:
            result = master.register_worker(worker_name, group,f"http://localhost:{worker_port}/")
            print(result)
    except ConnectionRefusedError:
        print(f"Error: Unable to connect to master at {master_port}.")

# Function to get the current load of the worker
def get_load():
    global requests_served
    return requests_served

# Function to retrieve records by name
def getbyname(name):
    global data_table
    global requests_served
    requests_served = requests_served + 1
    matching_records = []
    for record in data_table.values():
        if record.get('name') == name:
            matching_records.append(record)
    return {'error': False, 'result': matching_records}

# Function to retrieve records by location
def getbylocation(location):
    global data_table
    global requests_served
    requests_served = requests_served + 1
    matching_records = []
    for record in data_table.values():
        if record.get('location') == location:
            matching_records.append(record)
    return {'error': False, 'result': matching_records}

# Function to retrieve records by location and year
def getbyyear(location, year):
    global data_table
    global requests_served
    requests_served = requests_served + 1
    matching_records = []
    for record in data_table.values():
        if record.get('location') == location and record.get('year') == year:
            matching_records.append(record)
    return {'error': False, 'result': matching_records}

def main():
    if len(sys.argv) < 4:
        print('Usage: worker.py <master_address> <worker_name> <port> <group: am or nz>')
        sys.exit(0)

    master_port = sys.argv[1]  # Master server port
    worker_name = sys.argv[2]  # Worker name
    port = int(sys.argv[3])  # Worker server port
    group = sys.argv[4]  # Group name (am or nz)

    load_data(group)
    register_with_master(master_port, worker_name, port, group) # Registering with the master server

    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Worker {worker_name} listening on port {port}...")
    server.register_function(getbyname, 'getbyname')
    server.register_function(getbylocation, 'getbylocation')
    server.register_function(getbyyear, 'getbyyear')
    server.register_function(get_load, 'get_load')
    server.serve_forever()

if __name__ == '__main__':
    main()
