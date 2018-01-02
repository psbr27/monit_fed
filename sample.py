#!/usr/bin/env python
from multiprocessing import Process, Queue

import mysql_queries as mysql
import iptablelib
import portmanagerlib
import logmanager
import sys
import time
import linkedList
import sns

iptables = iptablelib.IpTablesLib('100.61.0.1', '10.1.1.199')
iptables.installIpTableNorth('10.1.1.77', 8000, 25000)
portmanager = portmanagerlib.PortManager()
log_m = logmanager.LogManager()
log = log_m.logger()
l = linkedList.LinkedList()


""" """
def install_iptables(sessions):
    for item in sessions:
        session = sessions[item]
        ssh_port = mysql.mysql_query_port_no(str(session['username']))
        iptables.installIpTableSouth(str(session['local_ip']), 22, ssh_port)
""" """
def delete_iptables(sessions):
    for item in sessions:
        session = sessions[item]
        ssh_port = mysql.mysql_query_reset_port_no(str(session['username']))
        iptables.deleteIpTableSouth(str(session['local_ip']), 22, ssh_port)
""" """
def query_esc_tbl():
    count = mysql.mysql_query_select_esc_tbl()
    return count

""" """
# Delete MySql data tables before start of the application
def cleanup_db():
    log.debug("Delete esc_tbl and esc_hbeat_tbl from escdb database")
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "DELETE FROM esc_tbl;"
    cursor.execute(sql)
    sql = "DELETE FROM esc_hbeat_tbl;"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()


""" """
def parse_connections(Q1):
    len_q = 0
    log.debug("Inside parser connections(P1) function")
    cleanup_db()
    drop_list = []
    list_count = 0
    connection_drop=False

    while True:
      sessions = Q1.get()
      len_q = (len(sessions))
      len_l = l.length()
      
      log.debug("Qlen: %d Llist: %d" %(len_q, len_l))
#fetch the number of sessions
#query the sql database
      count = query_esc_tbl() 
      if count is -1:
          log.debug("Reset ssh ports to ZERO")
          time.sleep(1)
          mysql.mysql_update_ssh_ports(sessions)
          log.debug("Insert data into esc_tbl")
          time.sleep(1)
          mysql.mysql_insert_query(sessions, True)
          install_iptables(sessions)
#Create linked  list of escs
          for item in sessions:
            l.add(item)
          l.printList() 
          continue


      if len_q == len_l:
#both queue and linked list have same number of sessions
          pass
      elif len_q > len_l:
#new session 
          for item in sessions:
            response = l.search(item)
            print(response)
            if response is None: 
              if 'UNDEF' not in str(item):
                l.add(item)
                log.debug("New connection %s" %(str(item)))
                new_list = mysql.mysql_query_esc_tbl(sessions)
                lenList = len(new_list)
                print(lenList)
                ssh_port = mysql.mysql_fetch_query_port_no(str(item))
                print("Assigned port is %d" %(ssh_port))
                print(sessions[item])
                newdata = sessions[item]
                if lenList > 0:
                  ssh_port = mysql.mysql_new_insert_query(newdata)
                  iptables.installIpTableSouth(str(newdata['local_ip']), 22, ssh_port)
                  status = mysql.mysql_get_deploy_status(newdata['username'])
                  if status == 0:
                    d_list = mysql.mysql_select_deploy_list(newdata['username'])
                    sns.notify_sms(newdata['username'],d_list[0],str(d_list[1]))
                    sns.notify_email(newdata['username'],d_list[0],str(d_list[1]))
                elif lenList == 0:
                  print("IP for connection is %s" %(str(newdata['local_ip'])))
                  iptables.installIpTableSouth(str(newdata['local_ip']), 22, ssh_port)
                else:
                  pass
                
      else:
#verify for connection drop
          for item in sessions:
            print(item)
            response = l.deleteNode(item)

          llist = l.printList()

          print(llist)
          
          for drop in llist:
            if drop is not 'UNDEF':
              ssh_port = mysql.mysql_fetch_query_port_no(str(drop))
              local_ip = mysql.mysql_query_local_ip(str(drop))
              print("Connection drop for %s port %s" %(local_ip, ssh_port))
              log.debug("Clean up iptable for %s IP: %s and port: %d" %(str(drop), str(local_ip), int(ssh_port)))
              iptables.deleteIpTableSouth(str(local_ip), 22, ssh_port)
              l.deleteNode(drop)

#update the list with sessions
          for item in sessions:
            l.add(item)
        
          #l.printList() 

#update the stats of client connections
      mysql.mysql_update_query(sessions,0)

