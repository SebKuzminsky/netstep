#!/usr/bin/env python3

import socketserver
import hal

class netstep_request_handler(socketserver.StreamRequestHandler):
    def handle(self):
        print(f"{self.client_address[0]}:{self.client_address[1]} connected")
        while True:
            self.data = self.rfile.readline().strip()
            if self.data == b'':
                print(f"{self.client_address[0]}:{self.client_address[1]} disconnected")
                break
            p = float(self.data)
            print(f"{self.client_address[0]}:{self.client_address[1]} set position-command to {p}")
            h['position-cmd'] = p

class netstep_tcp_server(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        self.allow_reuse_address = True
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

# connect to hal
h = hal.component("netstep")
h.newpin("position-cmd", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready() # mark the component as 'ready'

hal.connect("netstep.position-cmd", "position-cmd")

#try:
#    while 1:
#	# act on changed input pins; update values on output pins
#	time.sleep(1)
#	h['out'] = h['in']
#except KeyboardInterrupt: pass


HOST = "localhost"
PORT = 9999

# Create the server, binding to localhost on port 9999
with netstep_tcp_server((HOST, PORT), netstep_request_handler) as server:
    print(f"netstep ready at {HOST}:{PORT}")
    server.timeout = None
    server.serve_forever()
