import socket
import threading

class Client:
    def __init__(self):
        self.server = None
        self.soc = socket.socket()
        self.id = None

    def init_connection(self, ip, port):
        soc = socket.socket()
        soc.connect((ip, port))

        soc.send("Howdy".encode())
        
        self.id = int(soc.recv(1024).decode())
        self.soc.bind(('localhost', 13370+self.id))
        self.soc.listen()
        self.server = self.soc.accept()
        
    def talk_with_server(self):
        while True:
            message = self.server.recv(1024).decode()

            message = message.split(',')

            if len(message) == 3:
                print(f"Got new range {message[0]}-{message[1]} {message[2]}")
                # add the new range and delete previous

            elif len(message) == 2:
                print(f"Got finish message")
                # check if it's mine
                # celebrate
