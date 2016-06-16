from pydht import DHT
import sys
import os


class ChordNode():
    """docstring for ChordNode"""
    def __init__(self, address, port, hostip):
        self.address = address
        self.port = port
        self.hostip = hostip

    def join(self):
        if self.address == self.hostip:
            print "Only node in group"
            try:
                print "Starting server"
                dht = DHT(self.hostip, self.port)
                return dht
            except Exception, e:
                raise e

        else:
            print "Joining DHT group"
            try:
                print "Starting server"
                print self.hostip
                print self.port
                print self.address
                dht = DHT(self.hostip, self.port, boot_host=self.address, boot_port=self.port)
                return dht
            except Exception, e:
                raise e
