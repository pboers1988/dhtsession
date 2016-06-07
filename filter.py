from socket import AF_INET
import pynetfilter_conntrack

class Filter(object):
    """docstring for Filter"""
    def __init__(self):
        pass
    def filter(self ,tcpsocket):
        ct = pynetfilter_conntrack.Conntrack()
        try:
        	for ip in ct.dump_table(AF_INET):
	            name = tcpsocket.split(":")
	            print name
        except Exception, e:
        	raise e
