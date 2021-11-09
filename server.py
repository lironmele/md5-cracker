import hashlib
import socket
import threading
from typing import List

import range_conversion

ip = "0.0.0.0"
port = 13370

class Server:
    def __init__(self):
        self.clients = []
        self.ranges = []
        self.soc = socket.socket()
        self.id_count = 1

    def add_new_range(self, start, stop, md5):
        self.ranges = [*self.ranges, *range_conversion.get_ranges(start, stop, 100, md5)]
        print(f"Added range {start}-{stop} with md5: {md5}")

    def listen_for_new_connections(self):
        self.soc.bind(('localhost', 13370))
        self.soc.listen()

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
        client = Client(c_id=c_id, manager=self)
        client.connect((client_addr[0], port+c_id))

        self.clients.append(client)

        while True:
            client.communicate()

    def get_range(self):
        if len(self.ranges) > 0:
            return self.ranges.pop(0)
        else:
            return None

    def found(self, md5, password):
        hashed = hashlib.md5(password.encode()).hexdigest()
        if hashed != md5:
            return

        for n in range(len(self.ranges)):
            if self.ranges[n][2] == md5:
                self.ranges.pop(n)

        for c in self.clients:
            if c.searching == md5:
                c.found(md5)

    def handle_user_input(self):
        while True:
            input("Press enter to input more ranges")
            start = input("\tEnter start: ")
            stop = input("\tEnter stop: ")
            md5 = input("\tEnter MD5: ")
            self.add_new_range(start, stop, md5)
            print(f"{start},{stop},{md5} added to the queue")
            print()

class Client(socket.socket):
    def __init__(self, *args, **kwargs) -> None:
        self.c_id = kwargs.pop("c_id")
        self.manager: Server = kwargs.pop("manager")
        self.searching = False
        
        super(Client, self).__init__(*args, **kwargs)

    @classmethod
    def copy(cls, sock):
        fd = socket.dup(sock.fileno())
        copy = cls(sock.family, sock.type, sock.proto, fileno=fd)
        copy.settimeout(sock.gettimeout())
        return copy

    def communicate(self):
        if not self.searching:
            nrange = self.manager.get_range()
            
            while not nrange:
                nrange = self.manager.get_range()

            self.send(f"{nrange[0]},{nrange[1]},{nrange[2]}".encode())
            self.searching = nrange[2]
        else:
            message = self.recv(1024).decode()
            
            message = message.split(',')
            print(f'got {message}')

            if message[1] == 'true':
                self.manager.found(message[2], message[3])
            else:
                pass

            self.searching = False

    def found(self, md5):
        self.send(f"finish,{md5}".encode())
