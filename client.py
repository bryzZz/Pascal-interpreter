import zmq
import json
import sys


context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
  code_path = input('Path to your code: ')
  variant = int(input('Tree or Variables? (0 or 1): '))

  with open(code_path, 'r') as f:
    code = f.read()

    socket.send(code.encode())

    message = json.loads(socket.recv().decode())

    if variant == 0:
      print(message["tree"])
    else:
      print(message["variables"])
