"""
Hello World client in Python
Connects REQ socket to tcp://localhost:5555
Sends "Hello" to server, expects "World" back

note: requires argument naming the client
"""

import sys
import zmq

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit('usage: python hwserver.py <label>')
    label = args[0]
    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to hello world server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    #  Do 10 requests, waiting each time for a response
    for request in range(10):
        print("Sending request %s ..." % request)

        socket.send("Hello from {}".format(label).encode())
        #  Get the reply.
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))

main()