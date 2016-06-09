from socket import IPPROTO_TCP
import socket
import pynetfilter_conntrack
from pynetfilter_conntrack import *
from struct import *

class Filter(object):
    """docstring for Filter"""
    def __init__(self):
        pass

    @staticmethod
    def dump_table():
        try:
            ct = pynetfilter_conntrack.Conntrack()
            table,count = ct.dump_table(socket.AF_INET)
            return table
        except Exception, e:
            raise e
        

    @staticmethod
    def filter(ip, port, table):
        try:
            for entry in table:
                if ((entry.orig_l4proto == IPPROTO_TCP) and ((entry.tcp_state == TCP_CONNTRACK_ESTABLISHED) \
                    or (entry.tcp_state == TCP_CONNTRACK_LAST_ACK) or (entry.tcp_state == TCP_CONNTRACK_CLOSE_WAIT)) and (ip == str(entry.orig_ipv4_src)) and (port == entry.orig_port_src)):
                    print "Established connection"
                    print entry.tcp_state
                    return True # This connection is a "normal connction and should be passed to the application"
                elif (entry.orig_l4proto == IPPROTO_TCP and (ip == str(entry.orig_ipv4_src)) and (port == entry.orig_port_src)):
                    print entry.tcp_state
                    print "Not an Established connection"
                    return False
                else:
                    pass
        except Exception, e:
            raise e


    @staticmethod
    def newconn(ip, port, table):
        try:
            for entry in table:
                if ((entry.orig_l4proto == IPPROTO_TCP) and (entry.tcp_state == TCP_CONNTRACK_ESTABLISHED) and (ip == str(entry.orig_ipv4_src)) and (port == entry.orig_port_src)):
                    print entry.tcp_state
                    print "Syn packet With established connection"
                    return False
                elif ((entry.orig_l4proto == IPPROTO_TCP) and (entry.tcp_state == TCP_CONNTRACK_SYN_RECV) and (ip == str(entry.orig_ipv4_src)) and (port == entry.orig_port_src) ):
                    print entry.tcp_state
                    print "New Connection"
                    return True
                else:
                    pass
        except Exception, e:
            raise e

    @staticmethod
    def parser(buff, port=8080):
        ip_header = buff[0:20]
        iph = unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
         
        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
        
        tcp_header = buff[iph_length:iph_length+20]
     
        #now unpack them :)
        tcph = unpack('!HHLLBBHHH' , tcp_header) 
        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4
        
        flags = tcph[5]

        h_size = iph_length + tcph_length * 4
        data_size = len(buff) - h_size

        if (dest_port == port) and (protocol == 6) :  # Is the destination port that of the server and is the Protocol TCP (6)
            return [s_addr, source_port, sequence, acknowledgement, flags]
            print tcph
        else:
            return False