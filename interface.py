class Interface(object):
    """docstring for interface"""
    def __init__(self):
        pass
    
    def printing(self, result):
        return result

    def set(self, key, value, kserver):
        print "Setting key " + key + " and value " + value
        print kserver
        return kserver.set(str(key), str(value)).addCallback(self.printing)

    def get(self, key, kserver):
        print kserver
        return kserver.get(str(key)).addCallback(self.printing)