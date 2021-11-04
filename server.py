import socket
import threading
import hashlib
from typing import List

from range_conversion import str_to_num, num_to_str, get_ranges

ip = "0.0.0.0"
port = 13370
test = '9dcf6acc37500e699f572645df6e87fc'

class Server:
    def __init__(self):
        self.clients = []
        self.ranges = []
        self.soc = socket.socket()
    def add_new_range(self, start, stop, md5):
        self.ranges = [*self.ranges, *get_ranges(start, stop, 100, md5)]

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
        if hashed == md5:
            for c in self.clients:
                if c.searching == md5:
                    c.found(md5)

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
