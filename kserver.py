from twisted.application import service, internet
from twisted.python.log import ILogObserver
from twisted.internet import reactor, task
from twisted.python import log
from kademlia.network import Server
import os
import sys
import thread

class Kserver(object):
    """docstring for Kserver"""

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.dht = False
        self.get = False

    def kill(self):
        print "Killing the server"
        reactor.stop()

    def printing(self, result):
        print "Epic" + result

    @staticmethod
    def set(key, value, kserver):
        print "Setting key " + key + " and value " + value
        return kserver.set(str(key), str(value)).addCallback(printing)

    @staticmethod
    def get(key, kserver):
        return kserver.get(str(key)).addCallback(printing)

    def getserver(self):
        return self.dht

    def saveserver(self, found, kserver):
        self.dht = kserver

    def initkserver(self):
        #application = service.Application("kademlia")
        #pplication.setComponent(ILogObserver, log.FileLogObserver(sys.stdout, log.INFO).emit)
        log.startLogging(sys.stdout)
        if os.path.isfile('cache.pickle'):
            kserver = Server.loadState('cache.pickle')
            kserver.listen(self.port)
        else:
            kserver = Server()
            kserver.listen(self.port)
            kserver.bootstrap([(self.address, self.port)]).addCallback(self.saveserver, kserver)


        kserver.saveStateRegularly('cache.pickle', 10)
        
        try:    
            pid = os.fork()
        except Exception, e:
            raise e

        if (pid == 0):
            try:
                #reactor.listenUDP(self.port, kserver.protocol)
                reactor.run()
            except Exception, e:
                raise e

            # if (pid == 0):
            #     reactor.run()
            # else:
            #     os._exit(0)
        else:
            pass
