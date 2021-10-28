import socket
from typing import List

ip = "0.0.0.0"
port = 13370

class Server:
    def __init__(self):
        self.clients = []
        self.soc = socket.socket()
        self.id_count = 1

    def listen_for_new_connections(self):
        pass

    def add_new_patz(self, soc):
        pass

    def handle_clients(self):
        pass

    def send_horray(self):
        pass
