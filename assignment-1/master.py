from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys


workers = {
    'worker-1': ServerProxy("http://localhost:23001/"),
    'worker-2': ServerProxy("http://localhost:23002/")
}
      



def getbyname(name):
    # TODO
    global workers

    # Check the first letter of the name
    first_letter = name[0].lower()
    try:
        if first_letter >= 'a' and first_letter <= 'm':
            # Call worker-1 for names starting with A-M
            try:
                return workers['worker-1'].getbyname(name)
            except ConnectionRefusedError:
                return {'error': True, 'message': 'Worker-1 is unavailable'}
        elif first_letter >= 'n' and first_letter <= 'z':
            # Call worker-2 for names starting with N-Z
            try:
                return workers['worker-2'].getbyname(name)
            except ConnectionRefusedError:
                return {'error': True, 'message': 'Worker-2 is unavailable'}
        else:
            return {
                'error': True,
                'message': 'Invalid name'
        }
    except ConnectionRefusedError:
        return {'error': True, 'message': 'Worker is unavailable'}
    
def getbylocation(location):
    # TODO
    global workers
    try:
        # Send request to both workers to get data by location
        try:
            result_worker_1 = workers['worker-1'].getbylocation(location)
        except ConnectionRefusedError:
            return {'error': True, 'message': 'Worker-1 is unavailable'}
        try:
            result_worker_2 = workers['worker-2'].getbylocation(location)
        except ConnectionRefusedError:
            return {'error': True, 'message': 'Worker-2 is unavailable'}

        # Merge results from both workers
        merged_results = []
        merged_results.extend(result_worker_1['result'])
        merged_results.extend(result_worker_2['result'])
        print("in master get by location")

        return {
            'error': False,
            'result': merged_results
         }
    except ConnectionRefusedError:
        return {'error': True, 'message': 'Worker is unavailable'}

def getbyyear(location, year):
    # TODO
    global workers
    try:
        # Send request to both workers to get data by location and year
        try:
            result_worker_1 = workers['worker-1'].getbyyear(location, year)
        except ConnectionRefusedError:
            return {'error': True, 'message': 'Worker-1 is unavailable'}
        try:
            result_worker_2 = workers['worker-2'].getbyyear(location, year)
        except ConnectionRefusedError:
            return {'error': True, 'message': 'Worker-2 is unavailable'}

        # Merge results from both workers
        merged_results = []
        merged_results.extend(result_worker_1['result'])
        merged_results.extend(result_worker_2['result'])

        return {
            'error': False,
            'result': merged_results
         }   
    except ConnectionRefusedError:
        return {'error': True, 'message': 'Worker is unavailable'}

def main():
    port = int(sys.argv[1])
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    # TODO: register RPC functions
    server.register_function(getbyname, 'getbyname')
    server.register_function(getbylocation, 'getbylocation')
    server.register_function(getbyyear, 'getbyyear')
    server.serve_forever()


if __name__ == '__main__':
    main()