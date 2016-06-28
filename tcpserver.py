import socket
from struct import *
from ft import Filter
import os
import time
from chord import ChordSetter, ChordNode

class TCPServer():
    """docstring for TCPServer"""
    def __init__(self, address, hostip, chordport, port, anycast):
        self.address = address
        self.port = port
        self.hostip = hostip
        self.chordport = chordport
        self.anycast = anycast
        self.dht = None
        self.cache = {}

    def setcache(self, key, value):
        try:
            self.cache[key] = value
        except Exception, e:
            return e
        
    def getcache(self, key):
        try:
            return self.cache[key]
        except Exception, e:
            return None

    def initlistener(self):
        node = ChordNode(self.address, self.chordport, self.hostip)
        self.dht = node.join()

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except Exception, e:
            raise e
        try:
            while 1:
                buff, address = s.recvfrom(65535)

                packet_info = Filter.parser(buff, self.port)
                if packet_info is False:   # Check if its TCP or not
                    pass
                else:
                    table = Filter.dump_table()
                    if ((packet_info[3] != 0) and Filter.filter(packet_info[0], packet_info[1], table)): 
                     # Check if i the ack flag is set and if it is in the connection table
                        pass
                    elif((packet_info[3] != 0) and packet_info[0] == self.hostip):
                        packet = Filter.repack(buff, self.anycast)
                        sender = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
                        sender.sendto(packet, (self.anycast, 0))
                        print "Forwarded packet"
                    elif ((packet_info[3] != 0) and (Filter.filter(packet_info[0], packet_info[1], table) is False)):
                        print "ACK but not connected PANIC"                 
                        key = packet_info[0] +":" + str(packet_info[1])
                       
                        # see If we have the result in the cache
                        dest = self.getcache(key)
                        if dest is None:
                            dest = ChordSetter.getval(self.dht, key)
                            print "Dest is:", dest
                            self.setcache(key,dest)
                            print "Key is in chord"
                        else:
                            print "Key is in the cache"                     
                        print "The correct destination = " + dest
                        if dest == self.hostip:
                            packet = Filter.repack(buff, self.anycast)
                            sender = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
                            sender.sendto(packet, (self.anycast, 0))
                            print "Forwarded packet"
                        else:
                            packet = Filter.repack(buff, dest)
                            sender = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
                            sender.sendto(packet, (dest, 0))
                            print "Forwarded packet"


                    elif ((packet_info[3] == 0) and Filter.newconn(packet_info[0], packet_info[1], table)):
                        key = packet_info[0] +":" + str(packet_info[1])
                        value = self.hostip
                        print "Setting values"
                        ChordSetter.setval(self.dht, key, value)

                    elif ((packet_info[3] == 0) and ( Filter.newconn(packet_info[0], packet_info[1], table) is False)):
                        print "No Ack but no new connection. Passing to application"
                        pass

                    elif (int(packet_info[4]) % 2 == 1):
                        print "Fin"

                    elif ( conn.get(packet_info[0] +":" + str(packet_info[1])) ==  self.hostip):
                        print "Last Ack - Closed connection"

                    else:
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
                   c.send(l)
                   l = f.read(1024)
                f.close
                c.send('Done Sending')
                c.close()
                print "Done Sending"
        except Exception, e:
            raise e