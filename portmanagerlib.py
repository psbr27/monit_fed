from collections import deque
class PortManager(object):
    def __init__(self, port_range=(10000,60000)):
        self._available_ports = deque(range(port_range[0],port_range[1]))

    def getNextAvailablePort(self):
        return self._available_ports.popleft()
        #print 'get port'
        #print self._available_ports

    def returnPort(self,port):
        self._available_ports.append(port)
        #print 'return port'
        #print self._available_ports
       
    def returnPortList(self,portlist):
        self._available_ports.extend(portlist)
