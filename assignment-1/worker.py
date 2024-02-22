# Updated worker code with missing functions
from xmlrpc.server import SimpleXMLRPCServer
import sys
import json

# Storage of data
data_table = {}
requests_served = 0

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

def get_load():
    global data_table
    return len(data_table)

def getbyname(name):
    global data_table
    global requests_served
    requests_served = requests_served + 1
    matching_records = []
    for record in data_table.values():
        if record.get('name') == name:
            matching_records.append(record)
    return {'error': False, 'result': matching_records}

def getbylocation(location):
    global data_table
    global requests_served
    requests_served = requests_served + 1
    matching_records = []
    for record in data_table.values():
        if record.get('location') == location:
            matching_records.append(record)
    return {'error': False, 'result': matching_records}

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
    if len(sys.argv) < 3:
        print('Usage: worker.py <port> <group: am or nz>')
        sys.exit(0)

    port = int(sys.argv[1])
    group = sys.argv[2]
    load_data(group)
    print("Data loaded")
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Worker listening on port {port}...")
    server.register_function(getbyname, 'getbyname')
    server.register_function(getbylocation, 'getbylocation')
    server.register_function(getbyyear, 'getbyyear')
    server.register_function(get_load, 'get_load')
    server.serve_forever()

if __name__ == '__main__':
    main()
