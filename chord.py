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
                pid = os.fork()
            except Exception, e:
                raise e

            if (pid == 0):
                try:
                    print "Starting server"
                    dht = DHT(self.hostip, self.port)
                    return dht
                except Exception, e:
                    raise e
                finally:
                    os._exit(0)
            else:
                pass
        else:
            print "Joining DHT group"
            try:    
                pid = os.fork()
            except Exception, e:
                raise e

            if (pid == 0):
                try:
                    print "Starting server"
                    dht = DHT(self.hostip, self.port, boot_host=self.address, boot_port=self.port)
                    return dht
                except Exception, e:
                    raise e
                finally:
                    os._exit(0)
            else:
                pass
    