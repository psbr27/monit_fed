#!/usr/bin/env python
import threading
import re
import os 
import logmanager

ip_list=[]
ip_dict={}

log_m = logmanager.LogManager()
log = log_m.logger()



#ip class, concurrent pings for all active sessions
class ip_check(threading.Thread):
    def __init__ (self,ip, ip_dict):
        threading.Thread.__init__(self)
        self.ip = ip
        self.__successful_pings = -1
        self.ip_data = ip_dict

    def run(self):
        ping_out = os.popen("ping -q -c2 "+self.ip,"r")
        #print(ping_out)
        while True:
            line = ping_out.readline()
            if not line: break
            n_received = re.findall(received_packages,line)
            if n_received:
                self.__successful_pings = int(n_received[0])
                self.ip_data[self.ip] = "UP" 
                if self.__successful_pings == 0:
                      self.ip_data[self.ip] = "DOWN"

    def status(self):
        if self.__successful_pings == 0:
            return "no response"
        elif self.__successful_pings == 1:
            return "alive, but 50 % package loss"
        elif self.__successful_pings == 2:
            return "alive"
        else:
            return "shouldn't occur"

received_packages = re.compile(r"(\d) received")

def ping_response(ip_list, ip_dict):
    check_results = []
    for ip in ip_list:
        current = ip_check(ip, ip_dict)
        check_results.append(current)
        current.start()

    for el in check_results:
        el.join()

""" Process P2 """
def ping_connections(Q2, ping_res_dict):
    log.debug("+++ Created Ping Process (P2) +++")
    while True:
        del ip_list[:]
        ip_dict.clear() 
        sessions = Q2.get(True, 20)
        #print("[P2] Get success Q2")
        for item in sessions:
          data = sessions[item]
          ip_list.append(str(data['local_ip']))

        ping_response(ip_list, ip_dict)
        ping_res_dict.update(ip_dict)
