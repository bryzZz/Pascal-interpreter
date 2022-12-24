import zmq
import json
from ilib.interpreter import Interpreter

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

inter = Interpreter()

while True:
  message = socket.recv()
  print("Received request: %s" % message)

  tree, variables = inter.eval(message.decode())

  socket.send(json.dumps({"tree": str(tree), "variables": variables}).encode())
