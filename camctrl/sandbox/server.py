"""
Hello World server in Python
Binds REP socket to tcp://*:5555
Expects b"Hello" from client, replies with b"World"

note: requires argument naming server
"""

import sys
import time
import zmq

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit('usage: python hwserver.py <label>')
    label = args[0]
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    count = 0
    while True:
        count += 1
        #  Wait for next request from client
        message = socket.recv()
        print(type(message))
        print("Received request: {} {}".format(message, count))
        #  Do some 'work'
        time.sleep(1)
        #  Send reply back to client
        socket.send("{} {} {}".format(label, message, count).encode())

main()