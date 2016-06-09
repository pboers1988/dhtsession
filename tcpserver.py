import socket
from struct import *
from ft import Filter
import os


class TCPServer(object):
    """docstring for TCPServer"""
    def __init__(self, address, dht, hostip, port=8080):
        self.address = address
        self.port = port
        self.dht = dht
        self.hostip = hostip

    def initlistener(self):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except Exception, e:
            raise e
    #     return s

    # @staticmethod
    # def check_stream(self, s):
        # Create a Filter funtion
        
        try:
            while 1:
                buff, address = s.recvfrom(65535)

                packet_info = Filter.parser(buff, self.port)
                if packet_info is False:   # Check if its TCP or not
                    pass
                else:
                    if ((packet_info[3] != 0) and Filter.filter(packet_info[0], packet_info[1])):  # Check if i the ack flag is set and if it is in the connection table
                        print "Established or otherwise"
                        pass
                    elif ((packet_info[3] != 0) and (Filter.filter(packet_info[0], packet_info[1]) is False)):
                        print "ACK but not connected PANIC"
                        pass
                    elif ((packet_info[3] == 0) and ( Filter.newconn(packet_info[0], packet_info[1]) is False)):  
                        print "No Ack but no new connection. Passing to application"
                        print packet_info
                        pass
                    elif ((packet_info[3] == 0) and Filter.newconn(packet_info[0], packet_info[1])):
                        print "New Connection Storing key pair"
                        print  packet_info
                        print   
                        print
                        self.dht.set(packet_info[0] +":" + str(packet_info[1]), self.hostip)
                        pass
                    elif (int(packet_info[4]) % 2 == 1):
                        print "Fin Received"
                        pass
                    else:
                        print packet_info
                        print "Don't know whats going on here so doing a lookup and otherwise RST"
                        print self.dht.get(packet_info[0] +":" + str(packet_info[1]))
                        pass
        except Exception, e:
            raise e
