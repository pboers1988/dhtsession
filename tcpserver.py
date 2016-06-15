import socket
from struct import *
from ft import Filter
import os
#from kserver import Kserver
from chord import ChordClient
import time



class TCPServer():
    """docstring for TCPServer"""
    def __init__(self, address, hostip, chordport, port, anycast):
        self.address = address
        self.port = port
        self.hostip = hostip
        self.chordport = chordport
        self.anycast = anycast

    def initlistener(self):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except Exception, e:
            raise e

        client = ChordClient(self.address, self.chordport)
        conn = client.connection()
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
                        print conn.set(packet_info[0] +":" + str(packet_info[1]), self.hostip)

                    elif ((packet_info[3] == 0) and ( Filter.newconn(packet_info[0], packet_info[1], table) is False)):
                        print "No Ack but no new connection. Passing to application"
                    elif (int(packet_info[4]) % 2 == 1):
                        print "Fin Received"
                    elif ( conn.get(packet_info[0] +":" + str(packet_info[1])) ==  self.hostip):
                        print "Last Ack"
                    else:
                        print "Don't know whats going on here so doing a lookup and otherwise RST"
        except Exception, e:
            raise e


    def initserver(self):
        try:
            s = socket.socket()
            host = self.anycast
            port = self.port
            s.bind((host, port))
            s.listen(5)
            while True:
                c, addr = s.accept()
                print 'Got connection from', addr
                c.send('Thank you for your connecting')
                time.sleep(10)
                c.close()
        except Exception, e:
            raise e