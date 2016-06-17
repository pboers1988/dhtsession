from pydht import DHT
import sys
import os
import time
import cPickle as pickle

class ChordNode():
    """docstring for ChordNode"""
    def __init__(self, address, port, hostip):
        self.address = address
        self.port = port
        self.hostip = hostip

    def join(self):
        print "Starting DHT Overlay"
        if self.address == self.hostip:
            print "Only node in swarm"
            try:
                print "Starting server"
                dht = DHT(self.hostip, self.port)
                print "DHT started"
                return dht
            except Exception, e:
                raise e

        else:
            print "Joining DHT swarm"
            try:
                print "Starting server"
                dht = DHT(self.hostip, self.port, boot_host=self.address, boot_port=self.port)
                print "DHT started"
                return dht
            except Exception, e:
                print e

class ChordSetter():

    @staticmethod
    def getval(dht, key):
        print "Getting the host with key: " + key
        try:
            return dht[key]
        except Exception, e:
            print e

    @staticmethod
    def setval(dht, key, value):
        print "Setting the host with key: " + key + " and value: " + value
        try:
            dht[key] = value
            print "key set"
            print dht[key]
        except Exception, e:
            print e