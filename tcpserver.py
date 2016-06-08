import socket
from struct import *
from ft import Filter

class TCPServer(object):
    """docstring for TCPServer"""
    def __init__(self, address, port=8080):
        self.address = address
        self.port = port
        #self.dht = dht

    def initlistener(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except Exception, e:
            raise e

        # Create a Filter funtion
        while 1:
            buff, address = s.recvfrom(65535)

            packet_info = Filter.parser(buff, self.port)

            if packet_info is False:   # Check if its TCP or not
                pass
            else:
                print packet_info
                if ((packet_info[3] != 0) and Filter.filter(packet_info[0], packet_info[1])):  # Check if i the ack flag is set and if it is in the connection table
                    print "Established or otherwise"
                elif ((packet_info[3] != 0) and (Filter.filter(packet_info[0], packet_info[1]) is False)):
                    print "ACK but not connected PANIC"
                elif ((packet_info[3] == 0) and ( Filter.newconn(packet_info[0], packet_info[1]) is False)):  
                    print "No Ack but no new connection. Passing to application"
                elif ((packet_info[3] == 0) and Filter.newconn(packet_info[0], packet_info[1])):
                    print "No Ack but new connection. Initiliasing Three way hand shake"
                elif (int(packet_info[4]) % 2 == 1):
                    print "Fin Received"
                else:
                    print "Don't know whats going on here so doing a lookup and otherwise RST"