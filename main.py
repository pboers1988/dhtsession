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
    parser.add_argument('-c', type= str, required=True)
    args = parser.parse_args()

    #node = ChordNode(args.a, args.p, args.i)

    #node.start()


    tcpserver = TCPServer(args.a,  args.i, args.p, args.s, args.c)
    try:
         pid = os.fork()
    except Exception, e:
        raise e

    if (pid == 0):
        try:
            print "Starting Listener"
            tcpserver.initlistener()
        except Exception, e:
            raise e
        finally:
            os._exit(0)
    else:
        pass

    print "Starting Server"
    tcpserver.initserver()

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
 