#!/usr/bin/env python
import sys
import os
import argparse
from kserver import Kserver
from tcpserver import TCPServer
import socket
from chord import ChordNode
def main():
    # parse command line options
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default=7000)
    parser.add_argument('-a', type=str, required=True)
    parser.add_argument('-s', type=int, default=8080)
    parser.add_argument('-i', type=str, required=True)
    args = parser.parse_args()

    #kademlia = Kserver(args.a, args.p, args.i, args.s)
    #print "Starting kserver"
    #dht = kademlia.initkserver()

    #node = ChordNode(args.a, args.p, args.i)

    #node.start()


    tcpserver = TCPServer(args.a,  args.i, args.p, args.s)
    tcpserver.initlistener()

    # s.listen(1)
    # while 1:
    #     connection, client_address = s.accept()
    #     try:
    #         ip = client_address[0]
    #         cport = str(client_address[1])
    #         tcpsocket = ip + ":" + cport
    #         dht.set(tcpsocket, ip)
    #          ft = Filter()
    #          ft.filter(tcpsocket)
    #         # Receive the data in small chunks and retransmit it
    #         while True:
    #             data = connection.recv(16)
    #             print data
    #             if data:
    #                 connection.sendall(data)
    #             else:
    #                 print 'no more data from', client_address
    #                 break
    #     finally:
    #         # Clean up the connection
    #         connection.close()

    while True:
        pass
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
