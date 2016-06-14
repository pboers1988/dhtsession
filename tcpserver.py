import socket
from struct import *
from ft import Filter
import os
#from kserver import Kserver
from interface import Interface



class TCPServer():
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
        interface = Interface()
        try:
            while 1:
                buff, address = s.recvfrom(65535)

                packet_info = Filter.parser(buff, self.port)
                if packet_info is False:   # Check if its TCP or not
                    pass
                else:
                    table = Filter.dump_table()
                    print packet_info
                    if ((packet_info[3] != 0) and Filter.filter(packet_info[0], packet_info[1], table)):  # Check if i the ack flag is set and if it is in the connection table
                        print "Established or otherwise"
                    elif ((packet_info[3] != 0) and (Filter.filter(packet_info[0], packet_info[1], table) is False)):
                        print "ACK but not connected PANIC"
                    elif ((packet_info[3] == 0) and Filter.newconn(packet_info[0], packet_info[1], table)):
                        print packet_info[0] +":" + str(packet_info[1])
                        print self.hostip
                        #self.dht.set(packet_info[0] +":" + str(packet_info[1]), self.hostip)
                        print interface.set(packet_info[0] +":" + str(packet_info[1]), self.hostip, self.dht)

                    elif ((packet_info[3] == 0) and ( Filter.newconn(packet_info[0], packet_info[1], table) is False)):
                        print "No Ack but no new connection. Passing to application"
                    elif (int(packet_info[4]) % 2 == 1):
                        print "Fin Received"
                    else:
                        print packet_info
                        print "Don't know whats going on here so doing a lookup and otherwise RST"
                        print interface.get(packet_info[0] +":" + str(packet_info[1]), self.dht)
        except Exception, e:
            raise e
