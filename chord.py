from pydht import DHT
import sys
import os
import time

class ChordNode():
    """docstring for ChordNode"""
    def __init__(self, address, port, hostip):
        self.address = address
        self.port = port
        self.hostip = hostip
        self.dht = None

    def join(self):
        if self.address == self.hostip:
            print "Only node in group"
            try:
                print "Starting server"
                self.dht = DHT(self.hostip, self.port)
                self.dht['hi'] = ['hi2']
                print self.dht['hi']
            except Exception, e:
                raise e

        else:
            print "Joining DHT group"
            try:
                print "Starting server"
                self.dht = DHT(self.hostip, self.port, boot_host=self.address, boot_port=self.port)
                print self.dht['hi']
            except Exception, e:
                print e


    def getval(self, key):
        print "Getting the host with key: " + key
        try:
            print self.dht
            value = self.dht[key][0]
            time.sleep(1)
            return value
        except Exception, e:
            print e

    def setval(self, key, value):
        print "Setting the host with key: " + key + " and value: " + value
        try:
            print self.dht
            self.dht[key] = [value]
            print "If it was succesfull print this"
            time.sleep(2)
            self.dht["hi"] = ["hello"]
        except Exception, e:
            print e