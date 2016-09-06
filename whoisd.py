# coding: utf-8

import daemon
import socket
import socketserver
import threading

import settings

class WhoisHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.request.sendall(self.data.upper())

if __name__=="__main__":
    server = socketserver.TCPServer((settings.BIND_ADDRESS, settings.BIND_PORT), WhoisHandler)
    server.serve_forever()
