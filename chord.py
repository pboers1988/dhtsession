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
        if self.address == self.hostip:
            print "Only node in group"
            try:
                print "Starting server"
                dht = DHT(self.hostip, self.port)
                dht[u'hi'] = ['hi2']
                print dht
                return dht
            except Exception, e:
                raise e

        else:
            print "Joining DHT group"
            try:
                print "Starting server"
                dht = DHT(self.hostip, self.port, boot_host=self.address, boot_port=self.port)
                return dht
            except Exception, e:
                print e

class ChordSetter():

    @staticmethod
    def getval(dht, key):
        print "Getting the host with key: " + key
        try:
            print dht
            k = pickle.dumps(key)

            value = dht[k][0]
            time.sleep(1)
            return pickle.loads(value)
        except Exception, e:
            print e

    @staticmethod
    def setval(dht, key, value):
        print "Setting the host with key: " + key + " and value: " + value
        try:
            print key
            print value
            print "Setting......"
            dht[key] = [value]
            print "If it was succesfull print this"
            time.sleep(2)
            print dht[key]
            print "Slept"
        except Exception, e:
            print e