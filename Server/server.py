import socket
import threading
import hashlib
from typing import List

import BaseAscii
import RangeDivider

ip = "0.0.0.0"
port = 13370

class Server:
    def __init__(self):
        self.clients = []
        self.ranges = []
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

    def add_new_patz(self, c_id, client_addr):
        client = Client(c_id=c_id, manager=self, range=self.get_range())
        client.connect((client_addr, port+c_id))

        self.clients.append(client)

        client.communicate()

    def get_range(self, urange=None):
        if urange == None:
            for r in self.ranges:
                if not r:
                    return self.get_range(r)
        else:
            for r in urange.ranges:
                if not r:
                    return self.get_range(r)
            return urange

    def found(self, md5, password):
        hashed = hashlib.md5(password.encode()).hexdigest()
        if hashed == md5:
            for c in self.clients:
                if c.md5 == md5:
                    c.found()

class Client(socket.socket):
    def __init__(self, *args, **kwargs) -> None:
        super(Client, self).__init__(*args, **kwargs)
        
        self.c_id = kwargs["c_id"]
        self.manager: Server = kwargs["manager"]
        self.range = kwargs["range"]
        self.md5 = ""
        self.searching = False

    @classmethod
    def copy(cls, sock):
        fd = socket.dup(sock.fileno())
        copy = cls(sock.family, sock.type, sock.proto, fileno=fd)
        copy.settimeout(sock.gettimeout())
        return copy

    def communicate(self):
        pass

    def found(self):
        pass
