import socket
from filter import Filter

class TCPServer(object):
    """docstring for TCPServer"""
    def __init__(self, address, dht, port=8080):
        self.address = address
        self.port = port
        self.dht = dht

    def initsocketserver(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))
        s.listen(1)
        while 1:
            connection, client_address = s.accept()
            try:
                ip = client_address[0]
                cport = str(client_address[1])
                tcpsocket = ip + ":" + cport
                self.dht.set(tcpsocket, ip)
                ft = Filter()
                ft.filter(tcpsocket)
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    print data
                    if data:
                        connection.sendall(data)
                    else:
                        print 'no more data from', client_address
                        break
            finally:
                # Clean up the connection
                connection.close()
