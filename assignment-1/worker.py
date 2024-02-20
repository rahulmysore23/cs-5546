from xmlrpc.server import SimpleXMLRPCServer
import sys
import json

# Storage of data
data_table = {}


def load_data(group):
    # TODO load data based which portion it handles (am or nz)
    global data_table
    filename = f"data-{group}.json"
    print("Filename: '{filename}'")
    try:
        with open(filename, 'r') as file:
            data_table = json.load(file)
        print(f"Data loaded successfully for group {group}.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from file '{filename}'.")


def getbyname(name):
    # TODO
    global data_table
    matching_records = []
    for record in data_table.values():
        if record.get('name') == name:
            matching_records.append(record)

    return {
        'error': False,
        'result': matching_records
    }

def getbylocation(location):
    # TODO
    global data_table
    matching_records = []
    for record in data_table.values():
        if record.get('location') == location:
            matching_records.append(record)
    print("in worker get by location")

    return {
        'error': False,
        'result': matching_records
    }

def getbyyear(location, year):
    # TODO
    global data_table
    matching_records = []
    for record in data_table.values():
        if record.get('location') == location and record.get('year') == year:
            matching_records.append(record)

    return {
        'error': False,
        'result': matching_records
    }

def main():
    if len(sys.argv) < 3:
        print('Usage: worker.py <port> <group: am or nz>')
        sys.exit(0)

    port = int(sys.argv[1])
    group = sys.argv[2]
    load_data(group)
    print("Data loaded")
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    # TODO register RPC functions
    server.register_function(getbyname, 'getbyname')
    server.register_function(getbylocation, 'getbylocation')
    server.register_function(getbyyear, 'getbyyear')
    server.serve_forever()

if __name__ == '__main__':
    main()