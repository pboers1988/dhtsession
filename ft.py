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
                if ((entry.orig_l4proto == IPPROTO_TCP) and ((entry.tcp_state == TCP_CONNTRACK_ESTABLISHED) or (entry.tcp_state == TCP_CONNTRACK_LAST_ACK)\
                 or (entry.tcp_state == TCP_CONNTRACK_CLOSE_WAIT) or (entry.tcp_state == TCP_CONNTRACK_FIN_WAIT) or (entry.tcp_state == TCP_CONNTRACK_TIME_WAIT) \
                  or  (entry.tcp_state == TCP_CONNTRACK_CLOSE))\
                    and (ip == str(entry.orig_ipv4_src)) and (port == entry.orig_port_src)):
                    #print "Established connection, Closing or Time Wait"
                    return True # This connection is a "normal connction and should be passed to the application"
                elif (entry.orig_l4proto == IPPROTO_TCP):
                    print "Not an Established connection"
                    return False
        except Exception, e:
            raise e


    @staticmethod
    def newconn(ip, port, table):
        try:
            for entry in table:
                if ((entry.orig_l4proto == IPPROTO_TCP) and (entry.tcp_state == TCP_CONNTRACK_ESTABLISHED) and (ip == str(entry.orig_ipv4_src)) and (port == entry.orig_port_src)):
                    #print entry.tcp_state
                    print "Syn packet With established connection"
                    return False
                elif ((entry.orig_l4proto == IPPROTO_TCP) and (entry.tcp_state == TCP_CONNTRACK_SYN_RECV) and (ip == str(entry.orig_ipv4_src)) and (port == entry.orig_port_src) ):
                    print "New Connection"
                    return True
        except Exception, e:
            raise e

    @staticmethod
    def checksum(msg):
        s = 0
         
        # loop taking 2 characters at a time
        for i in range(0, len(msg), 2):
            w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
            s = s + w
         
        s = (s>>16) + (s & 0xffff);
        s = s + (s >> 16);
         
        #complement and mask to 4 byte short
        s = ~s & 0xffff
         
        return s

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
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])

        
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
            return [s_addr, source_port, sequence, acknowledgement, flags, d_addr]
        else:
            return False

    @staticmethod
    def repack(buff, dest):
        print "Repacking....."
        bufflength = len(buff)
        ip_header = buff[0:20]
        iph = unpack('!BBHHHBBH4s4s', ip_header)
        
        # Variables to make it repackable
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
         
        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        # Tcp stuff We Need this
        tcp_header = buff[iph_length:iph_length+20]

        print "I am about to unpack the TCP header"
        #now unpack them :)
        tcph = unpack('!HHLLBBHHH' , tcp_header) 
        print "That worked", tcph
        source_port = tcph[0]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4
        
        flags = tcph[5]

        h_size = iph_length + tcph_length * 4
        data_size = len(buff) - h_size
        data = buff[h_size:]

        print "Ip Header:", iph
        print "Dest", dest
        d_addr = socket.inet_aton(dest)

        print "Packing new Ip header"
        newiph = pack('!BBHHHBBH4s4s', iph[0], iph[1], iph[2], iph[3], iph[4], iph[5], iph[6],iph[7],iph[8],d_addr)
        print "Packed"

        try:
            packet = newiph + tcp_header + data
        except Exception, e:
            print e

        print "Calculating new checksum"
         
        try:
            check = Filter.checksum(packet)
            print "Calculated Checksum"
        except Exception, e:
            print "Calculation did not work"
            print e

        print "New TCP headers"
        tcp_doff = 5
        tcp_offset_res = (tcp_doff << 4) + 0
        try:
            newtcp_header = pack('!HHLLBBH', tcph[0], tcph[1], tcph[2],tcph[3],tcp_offset_res,tcph[5],tcph[6]) + pack('H', check) + pack('!H', tcph[8])
            print "Done"
        except Exception, e:
            print "Tcp header creation failed"
            print e

        packet = newiph + newtcp_header + data

        print "Passing to parser to double check the Header"
        print Filter.parser(packet)
        return packet
