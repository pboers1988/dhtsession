import socket
from struct import *
from ft import Filter
import os
#from kserver import Kserver
import time



class TCPServer():
    """docstring for TCPServer"""
    def __init__(self, address, hostip, chordport, port, anycast, dht):
        self.address = address
        self.port = port
        self.hostip = hostip
        self.chordport = chordport
        self.anycast = anycast
        self.dht = dht

    def initlistener(self):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except Exception, e:
            raise e

        client = ChordClient(self.hostip, self.chordport)
        conn = client.connection()
        try:
            while 1:
                buff, address = s.recvfrom(65535)

                packet_info = Filter.parser(buff, self.port)
                if packet_info is False:   # Check if its TCP or not
                    pass
                else:
                    table = Filter.dump_table()
                    if ((packet_info[3] != 0) and Filter.filter(packet_info[0], packet_info[1], table)):  # Check if i the ack flag is set and if it is in the connection table
                        print packet_info
                        print "Established, Closing or Time Wait"
                    elif ((packet_info[3] != 0) and (Filter.filter(packet_info[0], packet_info[1], table) is False)):
                        print "ACK but not connected PANIC"
                        print "Getting the right host"
                        
                        try:
                            dest = dht[packet_info[0] +":" + str(packet_info[1])]
                        except Exception, e:
                            raise e

                        print "The correct destination = " + dest
                        packet = Filter.repack(buff, dest)
                        sender = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                        sender.sendto(packet, (dest, 0))
                        print "Forwarded packet"
                    elif ((packet_info[3] == 0) and Filter.newconn(packet_info[0], packet_info[1], table)):
                        print packet_info
                        try:
                            dht[packet_info[0] +":" + str(packet_info[1])] = [self.hostip]
                        except Exception, e:
                            raise e
                    elif ((packet_info[3] == 0) and ( Filter.newconn(packet_info[0], packet_info[1], table) is False)):
                        print packet_info
                        print "No Ack but no new connection. Passing to application"
                    elif (int(packet_info[4]) % 2 == 1):
                        print "Fin"
                    elif ( conn.get(packet_info[0] +":" + str(packet_info[1])) ==  self.hostip):
                        print packet_info
                        print "Last Ack - Closed connection"
                    else:
                        print packet_info
                        print "Don't know whats going on here so doing a lookup and otherwise RST"
        except Exception, e:
            raise e


    def initserver(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = self.anycast
            port = self.port
            s.bind(('', port))
            s.listen(5)
            while True:
                c, addr = s.accept()
                print 'Got connection from', addr
                c.send("""\
HTTP/1.1 200 OK
""")
                f = open('/root/2gig.bin','rb')
                l = f.read(1024)
                while l:
                    print 'Sending...'
                    c.send(l)
                    l = f.read(1024)
                f.close
                c.send('Done Sending')
                c.close()
                print "Done Sending"
        except Exception, e:
            raise e