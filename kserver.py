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

    def kill(self):
        print "Killing the server"
        reactor.stop()

    @staticmethod
    def set(key, value, kserver):
        print "Setting key " + key + " and value " + value
        kserver.saveState('cache.pickle')
        return kserver.set(str(key), str(value))

    @staticmethod
    def get(key, kserver):
        return kserver.get(str(key))

    def initkserver(self):
        #application = service.Application("kademlia")
        #pplication.setComponent(ILogObserver, log.FileLogObserver(sys.stdout, log.INFO).emit)
        log.startLogging(sys.stdout)
        if os.path.isfile('cache.pickle'):
            kserver = Server.loadState('cache.pickle')
            kserver.listen(self.port)
        else:
            kserver = Server()
            kserver.bootstrap([(self.address, self.port)])
            kserver.listen(self.port)

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

        return kserver
