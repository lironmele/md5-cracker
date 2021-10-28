import socket
import threading
from typing import List

ip = "0.0.0.0"
port = 13370

class Server:
    def __init__(self):
        self.clients = []
        self.soc = socket.socket()
        self.id_count = 1

    def listen_for_new_connections(self):
        while True:
            client, client_addr = self.soc.accept()

            try:
                message = client.recv(1024).decode()
            except:
                continue

            if message != 'Howdy':
                continue

            client.send(str(self.id_count).encode())

            threading.Thread(target=self.add_new_patz, args=(self.id_count, client_addr)).start()

            self.id_count += 1

    def add_new_patz(self, id, client_addr):
        client = socket.socket()
        client.connect((client_addr, port+id))

        self.clients.append(client)

    def handle_clients(self):
        pass

    def send_horray(self):
        pass
