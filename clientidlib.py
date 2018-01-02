from collections import deque
class clientID(object):
    def __init__(self, port_range=(0,300)):
        self._available_ports = deque(range(port_range[0],port_range[1]))

    def getNextAvailableId(self):
        return self._available_ports.popleft()
        #print 'get port'
        #print self._available_ports

    def returnId(self,port):
        self._available_ports.append(port)
        #print 'return port'
        #print self._available_ports
       
    def returnIdList(self,portlist):
        self._available_ports.extend(portlist)
