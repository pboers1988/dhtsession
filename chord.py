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
                dht = DHT(self.hostip, self.port, boot_host=self.address, boot_port=self.port)
                return dht
            except Exception, e:
                raise e


    @staticmethod
    def get(dht, key):
        print "Getting the host with key: " + key
        try:
            value = dht[key][0]
            time.sleep(1)
            return value
        except Exception, e:
            return e

    @staticmethod
    def set(dht, key, value):
        print "Setting the host with key: " + key + "and value: " + value
        try:
            dht[key] = [value]
            time.sleep(2)
        except Exception, e:
            return e