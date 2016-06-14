from chorddht.node import Node  
from chorddht.client import ChordConnection
import sys
import os


class ChordNode():
    """docstring for ChordNode"""
    def __init__(self, address, port, hostip):
        self.address = address
        self.port = port
        self.hostip = hostip

    def join(self, node):
        if self.address == self.hostip:
            print "Only node in group"
        else:
            print "Joining group"
            bind_addr = self.address + ":" + str(self.port)
            node.join(bind_addr)

    def start(self):
        bind_addr = self.hostip + ":" + str(self.port)
        try:    
            pid = os.fork()
        except Exception, e:
            raise e

        if (pid == 0):
            try:
                print "Starting server"
                node = Node(bind_addr)
                self.join(node)
            except Exception, e:
                raise e
        else:
            pass

class ChordClient():
    """docstring for ChordClient"""
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def connection(self):
        conn_addr = self.address + ":" + str(self.port)
        return ChordConnection(conn_addr)       