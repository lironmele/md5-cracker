import socket
import threading
import range_conversion
import hashlib

class Client:
    def __init__(self):
        self.server = None
        self.soc = socket.socket()
        self.cracker = Cracker()
        self.id = None

    def init_connection(self, ip, port):
        soc = socket.socket()
        soc.connect((ip, port))

        soc.send("Howdy".encode())
        
        self.id = int(soc.recv(1024).decode())
        self.soc.bind(('localhost', 13370+self.id))
        self.soc.listen()
        self.server, _ = self.soc.accept()
        
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

    def add_new_range(self, start, stop, md5):
        ranges = range_conversion.get_ranges(start, stop, 10, md5)

        for r in ranges:
            # create new thread
            # give it a way to alert if found
            print(f"Start range {r[0]}-{r[1]}")
            threading.Thread(target=self.cracker.crack, args=(r[0], r[1], r[2], self.found)).start()

    def found(self, md5, password):
        print(f"Found password {password}")
        self.server.send(f"found,{self.id},{md5},{password}".encode())

class Cracker:
    def __init__(self):
        self.stop = False

    def crack(self, start, stop, md5, found):
        current = start
        current_num = range_conversion.str_to_num(start)
        padding = len(start)
        
        while not self.stop and start != stop:
            if hashlib.md5(current.encode()).hexdigest() == md5:
                found(md5, current)
                return
            else:
                current_num += 1
                current = range_conversion.num_to_str(current_num, padding)
