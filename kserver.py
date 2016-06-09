from twisted.application import service, internet
from twisted.python.log import ILogObserver
from twisted.internet import reactor, task
from twisted.python import log
from kademlia.network import Server
from kademlia import log
import os
import sys
import thread

class Kserver(object):
    """docstring for Kserver"""

    def __init__(self, address, port):
        self.address = address
        self.port = port

    def kill(self):
        print "Killing the server"
        reactor.stop()

    def set(self, key, value):
        self.kserver.set(key, value)

    def get(self, key):
        return self.kserver.get(key)

    def initkserver(self):
        application = service.Application("kademlia")
        application.setComponent(ILogObserver, log.FileLogObserver(sys.stdout, log.INFO).emit)
        if os.path.isfile('cache.pickle'):
            kserver = Server.loadState('cache.pickle')
            kserver.listen(self.port)
        else:
            kserver = Server()
            kserver.bootstrap([(self.address, self.port)])
            #kserver.listen(self.port)

        kserver.saveStateRegularly('cache.pickle', 10)
        
        try:
            pid = os.fork()
        except Exception, e:
            raise e

        if (pid == 0):
            try:
                reactor.listenUDP(self.port, kserver.protocol)
                reactor.run()
            except Exception, e:
                raise e

            # if (pid == 0):
            #     reactor.run()
            # else:
            #     os._exit(0)
        else:
            pass

        self.kserver = kserver
        return kserver
