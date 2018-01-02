
import subprocess

class IpTablesLib(object):
    def __init__(self, mtep_vpn_ip, mtep_vpc_ip, vpc_interface="eth0", vpn_interface="tun0"):
        self._vpc_interface = vpc_interface
        self._vpn_interface = vpn_interface
        self._mtep_vpn_ip = mtep_vpn_ip
        self._mtep_vpc_ip = mtep_vpc_ip
        self._north_bound_port_range = (64000,65000)


    def installPreRouteSouth(self,iap_ip, iap_port, mtep_port):
        #create prerouting rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("-I")
        command_list.append("PREROUTING")
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("-i")
        command_list.append(self._vpc_interface)
        command_list.append("--dport")
        command_list.append(str(mtep_port))
        command_list.append("-j")
        command_list.append("DNAT")
        command_list.append("--to")
        command_list.append(iap_ip + ":" + str(iap_port))
        subprocess.check_call(command_list)
        del command_list
    
    def installPostRouteSouth(self,iap_ip, iap_port, mtep_port):
        #create postrouting rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("-I")
        command_list.append("POSTROUTING")
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("-o")
        command_list.append(self._vpn_interface)
        command_list.append("--dport")
        command_list.append(str(iap_port))
        command_list.append("-j")
        command_list.append("SNAT")
        command_list.append("--to-source")
        command_list.append(self._mtep_vpn_ip)
        subprocess.check_call(command_list) 
        del command_list
    
    def installForwardRouteSouth(self,iap_port):    
        #create forwarding rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-A")
        command_list.append("FORWARD")
        command_list.append("-i")
        command_list.append(self._vpc_interface)
        command_list.append("-o")
        command_list.append(self._vpn_interface)
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("--dport")
        command_list.append(str(iap_port))
        command_list.append("-j")
        command_list.append("ACCEPT")
        subprocess.check_call(command_list) 
        del command_list
    
    
    def installIpTableSouth(self, iap_ip, iap_port, mtep_port):
    #install iptable rules
        self.installPreRouteSouth(iap_ip, iap_port, mtep_port)
        self.installPostRouteSouth(iap_ip, iap_port, mtep_port)
        self.installForwardRouteSouth(iap_port)    
    
    def deletePreRouteSouth(self,iap_ip, iap_port, mtep_port):
        #create prerouting rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("-D")
        command_list.append("PREROUTING")
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("-i")
        command_list.append(self._vpc_interface)
        command_list.append("--dport")
        command_list.append(str(mtep_port))
        command_list.append("-j")
        command_list.append("DNAT")
        command_list.append("--to")
        command_list.append(iap_ip + ":" + str(iap_port))
        subprocess.check_call(command_list)
        del command_list
    
    def deletePostRouteSouth(self,iap_ip, iap_port, mtep_port):
        #create postrouting rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("-D")
        command_list.append("POSTROUTING")
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("-o")
        command_list.append(self._vpn_interface)
        command_list.append("--dport")
        command_list.append(str(iap_port))
        command_list.append("-j")
        command_list.append("SNAT")
        command_list.append("--to-source")
        command_list.append(self._mtep_vpn_ip)
        subprocess.check_call(command_list) 
        del command_list
    
    def deleteForwardRouteSouth(self,iap_port):    
        #create forwarding rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-D")
        command_list.append("FORWARD")
        command_list.append("-i")
        command_list.append(self._vpc_interface)
        command_list.append("-o")
        command_list.append(self._vpn_interface)
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("--dport")
        command_list.append(str(iap_port))
        command_list.append("-j")
        command_list.append("ACCEPT")
        subprocess.check_call(command_list) 
        del command_list
    
    
    def deleteIpTableSouth(self, iap_ip, iap_port, mtep_port):
    #install iptable rules
        self.deletePreRouteSouth(iap_ip, iap_port, mtep_port)
        self.deletePostRouteSouth(iap_ip, iap_port, mtep_port)
        self.deleteForwardRouteSouth(iap_port)   





############# North Bound Rules #####################################
    def installPreRouteNorth(self,aws_ip, aws_port, mtep_port):
        #create prerouting rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("-I")
        command_list.append("PREROUTING")
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("-i")
        command_list.append(self._vpn_interface)
        command_list.append("--dport")
        command_list.append(str(mtep_port))
        command_list.append("-j")
        command_list.append("DNAT")
        command_list.append("--to")
        command_list.append(aws_ip + ":" + str(aws_port))
        subprocess.check_call(command_list)
        del command_list
    
    def installPostRouteNorth(self,aws_ip, aws_port, mtep_port):
        #create postrouting rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("-I")
        command_list.append("POSTROUTING")
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("-o")
        command_list.append(self._vpc_interface)
        command_list.append("--dport")
        command_list.append(str(aws_port))
        command_list.append("-j")
        command_list.append("SNAT")
        command_list.append("--to-source")
        #command_list.append(self._mtep_vpc_ip)
        command_list.append(self._mtep_vpc_ip + ':' + str(self._north_bound_port_range[0]) + '-' + str(self._north_bound_port_range[1]))
        subprocess.check_call(command_list) 
        del command_list
    
    def installForwardRouteNorth(self,aws_port):    
        #create forwarding rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-A")
        command_list.append("FORWARD")
        command_list.append("-i")
        command_list.append(self._vpn_interface)
        command_list.append("-o")
        command_list.append(self._vpc_interface)
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("--dport")
        command_list.append(str(aws_port))
        command_list.append("-j")
        command_list.append("ACCEPT")
        subprocess.check_call(command_list) 
        del command_list
    
    
    def installIpTableNorth(self, aws_ip, aws_port, mtep_port):
    #install iptable rules
        self.installPreRouteNorth(aws_ip, aws_port, mtep_port)
        self.installPostRouteNorth(aws_ip, aws_port, mtep_port)
        self.installForwardRouteNorth(aws_port)    
    
    def deletePreRouteNorth(self,aws_ip, aws_port, mtep_port):
        #delete prerouting rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("-D")
        command_list.append("PREROUTING")
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("-i")
        command_list.append(self._vpn_interface)
        command_list.append("--dport")
        command_list.append(str(mtep_port))
        command_list.append("-j")
        command_list.append("DNAT")
        command_list.append("--to")
        command_list.append(aws_ip + ":" + str(aws_port))
        subprocess.check_call(command_list)
        del command_list
    
    def deletePostRouteNorth(self,aws_ip, aws_port, mtep_port):
        #delete postrouting rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("-D")
        command_list.append("POSTROUTING")
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("-o")
        command_list.append(self._vpc_interface)
        command_list.append("--dport")
        command_list.append(str(aws_port))
        command_list.append("-j")
        command_list.append("SNAT")
        command_list.append("--to-source")
        command_list.append(self._mtep_vpc_ip + ':' + str(self._north_bound_port_range[0]) + '-' + str(self._north_bound_port_range[1]))
        #command_list.append(self._mtep_vpc_ip)
        subprocess.check_call(command_list) 
        del command_list
    
    def deleteForwardRouteNorth(self,aws_port):    
        #delete forwarding rule
        command_list = []
        command_list.append("iptables")
        command_list.append("-D")
        command_list.append("FORWARD")
        command_list.append("-i")
        command_list.append(self._vpn_interface)
        command_list.append("-o")
        command_list.append(self._vpc_interface)
        command_list.append("-p")
        command_list.append("tcp")
        command_list.append("--dport")
        command_list.append(str(aws_port))
        command_list.append("-j")
        command_list.append("ACCEPT")
        subprocess.check_call(command_list) 
        del command_list
    
    
    def deleteIpTableNorth(self, aws_ip, aws_port, mtep_port):
    #delete iptable rules
        self.deletePreRouteNorth(aws_ip, aws_port, mtep_port)
        self.deletePostRouteNorth(aws_ip, aws_port, mtep_port)
        self.deleteForwardRouteNorth(aws_port)    

#### DELETE ALL RULES ###
    def deleteIpTable(self):
        command_list=[]
        command_list.append("iptables")
        command_list.append("--flush")
        subprocess.check_call(command_list)
        del command_list
        command_list=[]
        command_list.append("iptables")
        command_list.append("-t")
        command_list.append("nat")
        command_list.append("--flush")
        subprocess.check_call(command_list)
        del command_list
