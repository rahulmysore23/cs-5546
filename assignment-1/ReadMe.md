# Distributed Master Client 

## Prerequisite

This program will need the below - 
-  Python 
- Ports 8000, 23001, 23002, 23003, 23004 free on the system. (The ports can be changed based on user preference, but needs changes to the commands below)

## Execution

> Note: Run each command in a separate terminal instance/tab

Follow the steps in the order mentioned below: 

1. Start the master server with the command below
```bash
python3 master.py 8000
 ```
2. Start the workers now. Let's start with worker 1 instance 1. Run the below command to start it. 
```bash
python3 worker.py 8000 w1-1 23001 am
 ```
3. Run the below command to start worker 1 instance 2
```bash
python3 worker.py 8000 w1-2 23002 am
 ```
4. Let's start worker 2 instance 1. Run the below command to start it. 
```bash
python3 worker.py 8000 w2-1 23003 nz
 ```
5. Run the below command to start worker 2 instance 2
```bash
python3 worker.py 8000 w2-2 23004 nz
 ```
6. Now run the client using the below command
```bash
python3 client.py 8000
```