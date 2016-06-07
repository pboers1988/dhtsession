#!/usr/bin/env python
import sys
import os
import argparse
from kserver import Kserver
from tcpserver import TCPServer
from filter import Filter
import socket

def main():
    # parse command line options
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default=7000)
    parser.add_argument('-a', type=str, required=True)
    args = parser.parse_args()

    kademlia = Kserver(args.a, args.p)
    dht = kademlia.initkserver()
    #tcpserver = TCPServer(args.a, dht, args.p)
    #tcpserver.initsocketserver()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((args.a, 8080))
    s.listen(1)
    while 1:
        connection, client_address = s.accept()
        try:
            ip = client_address[0]
            cport = str(client_address[1])
            tcpsocket = ip + ":" + cport
            dht.set(tcpsocket, ip)
            ft = Filter()
            ft.filter(tcpsocket)
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print data
                if data:
                    connection.sendall(data)
                else:
                    print 'no more data from', client_address
                    break
        finally:
            # Clean up the connection
            connection.close()

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
