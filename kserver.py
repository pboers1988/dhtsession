from twisted.application import service, internet
from twisted.python.log import ILogObserver
from twisted.internet import reactor, task
from twisted.python import log
from kademlia.network import Server
import os
import sys
import thread
from tcpserver import TCPServer

class Kserver():
    """docstring for Kserver"""
    def __init__(self, address, port, hostip, listen):
        self.address = address
        self.port = port
        self.hostip = hostip
        self.listen = listen

    def kill(self):
        print "Killing the server"
        reactor.stop()

    def printing(self, result):
        print "Epic" + result


    def startTCP(self, found, dht):
        tcpserver = TCPServer(self.address, dht, self.hostip, self.listen)
        tcpserver.initlistener()


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
            kserver.bootstrap([(self.address, self.port)]).addCallback(self.startTCP, kserver)


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
