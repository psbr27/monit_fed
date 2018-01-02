#!/usr/bin/env python

import Queue
import threading
import time

import logmanager
import snmp_stat as snmp
import mysql_queries as mysql
import trap_v2c as snmp_trap
import multiprocessing

log_m = logmanager.LogManager()
log = log_m.logger()
heart_beat_counter = 0
heart_beat_dict = {'esc_sn030': 0, 'esc_sn01':0,'esc_sn015':0,'esc_sn023':0,'esc_sn026':0,'esc_sn029':0,'esc_sn08':0,'esc_sn014':0, 'esc_sn010':0,'esc_sn024':0, 'esc_sn021':0}
signal_list = []


esc_01_Q = multiprocessing.Queue(100)
esc_015_Q = multiprocessing.Queue(100)
esc_021_Q = multiprocessing.Queue(100)
esc_023_Q = multiprocessing.Queue(100)
esc_026_Q = multiprocessing.Queue(100)
esc_029_Q = multiprocessing.Queue(100)
esc_08_Q = multiprocessing.Queue(100)
esc_010_Q = multiprocessing.Queue(100)
esc_014_Q = multiprocessing.Queue(100)
esc_024_Q = multiprocessing.Queue(100)
esc_030_Q = multiprocessing.Queue(100)

thread_list = []
hb_interval = 45

# sensor id is different because it is coming from ESC, where as
# other id is from openvpn
#=====o======o=====o======o=====o======o=====o======o=====
def put_data_into_queue(username, data):
    escQ = username[4:] + "_Q"
    eval(escQ).put(data)


#=====o======o=====o======o=====o======o=====o======o=====
def esc_thread_handler(username, city):
    q_thread = username + "__q_thread"
    escQ = username + "_Q"
    esc_worker = multiprocessing.Process(target=eval(q_thread), args=(username,))
    esc_worker.start()


# o==================================o====================================o================================
# ESC SN 029
# o==================================o====================================o================================
def esc_sn029_handler(username, Q):
    count = 0
    long(count)
    log.debug("Timer invoked esc_sn029_handler every 15sec")
    log.debug("Size of esc_sn029 queue %d" %(Q.qsize()))
    if esc_sn029_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn029, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(29, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        count = count + 1
        log.debug('Fetch data from esc_sn029_Q')
        esc_sn029_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        mysql.mysql_update_hb_count(count, username)
        snmp.snmp_set_operations(29, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_sn029_Q.task_done()
        heart_beat_counter = 0

def esc_sn029__q_thread(username, queue):
    #with signal.NewQueue(29) as queue:
      log.debug("Created esc_sn029__q_thread")
      thread_list.append(username)
      
      while True:
        log.debug("#29: Waiting for the queue data")
        data = queue.get(True, 15)
        if data is None:
          #increase the hb counter
          log.debug(data)
        else:
          log.debug("Heart beat Rx for esc_sn029")
          
        

# o==================================o====================================o================================
# ESC SN 026
# o==================================o====================================o================================
def esc_sn026_handler(username):
    count = 0
    long(count)
    log.debug("Timer invoked esc_sn026_handler every 15sec")
    log.debug("Size of esc_sn026 queue %d" %(esc_sn026_Q.qsize()))
    if esc_sn026_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn026, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(26, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        count = count + 1
        log.debug('Fetch data from esc_sn026_Q')
        esc_sn026_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        snmp.snmp_set_operations(26, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        mysql.mysql_update_hb_count(count, username)
        esc_sn026_Q.task_done()
        heart_beat_counter = 0

def esc_sn026__q_thread(username):
    log.debug("Created esc_sn026__q_thread")
    thread_list.append(username)
    while True:
        t2 = threading.Timer(15.0, esc_sn026_handler, args=(username,))
        t2.setName("esc_sn026__q_thread")
        t2.start() #after 15 seconds, trigger esc_sn029_handler
        time.sleep(15)
        t2.cancel()

# o==================================o====================================o================================
# ESC SN 024
# o==================================o====================================o================================
def esc_sn024_handler(username):
    count = 0
    log.debug("Timer invoked esc_sn024_handler every 15sec")
    log.debug("Size of esc_sn024 queue %d" %(esc_sn024_Q.qsize()))
    if esc_sn024_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn024, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(24, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        log.debug('Fetch data from esc_sn024_Q')
        esc_sn024_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        snmp.snmp_set_operations(24, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_sn024_Q.task_done()
        heart_beat_counter = 0

def esc_sn024__q_thread(username):
    log.debug("Created esc_sn024__q_thread")
    thread_list.append(username)
    while True:
        t2 = threading.Timer(15.0, esc_sn024_handler, args=(username,))
        t2.setName("esc_sn024__q_thread")
        t2.start() #after 15 seconds, trigger esc_sn024_handler
        time.sleep(15)
        t2.cancel()


# o==================================o====================================o================================
# ESC SN 023
# o==================================o====================================o================================
def esc_sn023_handler(username, Q):
    count = 0
    log.debug("Timer invoked esc_sn023_handler every 15sec")
    log.debug("Size of esc_sn023 queue %d" %(Q.qsize()))
    log.debug(Q)
    if Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn023, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(23, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        log.debug('Fetch data from esc_023_Q')
        Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        snmp.snmp_set_operations(23, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        Q.task_done()
        heart_beat_counter = 0

#
def esc_sn023__q_thread(username):
    #with signal.NewQueue(23) as queue:
      log.debug(esc_023_Q)
      log.debug("Created esc_sn023__q_thread")
      thread_list.append(username)

      while True:
        log.debug("#23: Waiting for the queue data")
        try:
          data = esc_023_Q.get(True, 15) 
        except Queue.Empty:
          log.debug("#23: Queue empty")
        else:
          log.debug("Heart beat Rx for esc_sn023")
 

# o==================================o====================================o================================
# ESC SN 021
# o==================================o====================================o================================
def esc_sn021_handler(username):
    count = 0
    log.debug("Timer invoked esc_sn021_handler every 15sec")
    log.debug("Size of esc_sn021 queue %d" %(esc_021_Q.qsize()))
    if esc_021_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn021, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(21, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        log.debug('Fetch data from esc_021_Q')
        esc_021_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        snmp.snmp_set_operations(21, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_021_Q.task_done()
        heart_beat_counter = 0

#
def esc_sn021__q_thread(username):
    #with signal.NewQueue(21) as queue:
      log.debug(esc_021_Q)
      log.debug("Created esc_sn021__q_thread")
      thread_list.append(username)
      
      while True:
        log.debug("#21: Waiting for the queue data")
        try:
          data = esc_021_Q.get(True, 15) 
        except Queue.Empty:
          log.debug("#21: Queue empty")
        else:
          log.debug("Heart beat Rx for esc_sn021")
 

# o==================================o====================================o================================
# ESC SN 015
# o==================================o====================================o================================
def esc_sn015_handler(username):
    count = 0
    log.debug("Timer invoked esc_sn015_handler every 15sec")
    log.debug("Size of esc_sn015 queue %d" %(esc_sn015_Q.qsize()))
    if esc_sn015_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn015, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(15, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        log.debug('Fetch data from esc_sn015_Q')
        esc_sn015_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        snmp.snmp_set_operations(15, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_sn015_Q.task_done()
        heart_beat_counter = 0

#
def esc_sn015__q_thread(username):
    log.debug("Created esc_sn015__q_thread")
    thread_list.append(username)
    while True:
        t2 = threading.Timer(15.0, esc_sn015_handler, args=(username,))
        t2.setName("esc_sn015__q_thread")
        t2.start() #after 15 seconds, trigger esc_sn015_handler
        time.sleep(15)
        t2.cancel()


# o==================================o====================================o================================
# ESC SN 014
# o==================================o====================================o================================
def esc_sn014_handler(username):
    count = 0
    long(count)
    log.debug("Timer invoked esc_sn014_handler every 15sec")
    log.debug("Size of esc_sn014 queue %d" %(esc_sn014_Q.qsize()))
    if esc_sn014_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn014, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(14, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        count = count + 1
        log.debug('Fetch data from esc_sn015_Q')
        esc_sn014_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        mysql.mysql_update_hb_count(count, username)
        snmp.snmp_set_operations(14, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_sn014_Q.task_done()
        heart_beat_counter = 0

#
def esc_sn014__q_thread(username):
    log.debug("Created esc_sn014__q_thread")
    thread_list.append(username)
    while True:
        t2 = threading.Timer(15.0, esc_sn014_handler, args=(username,))
        t2.setName("esc_sn014__q_thread")
        t2.start() #after 15 seconds, trigger esc_sn014_handler
        time.sleep(15)
        t2.cancel()



# o==================================o====================================o================================
# ESC SN 08
# o==================================o====================================o================================
def esc_sn08_handler(username):
    count = 0
    log.debug("Timer invoked esc_sn08_handler every 15sec")
    log.debug("Size of esc_sn08 queue %d" %(esc_08_Q.qsize()))
    if esc_08_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn08, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(8, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        log.debug('Fetch data from esc_08_Q')
        esc_08_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        snmp.snmp_set_operations(8, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_08_Q.task_done()
        heart_beat_counter = 0

#
def esc_sn08__q_thread(username):
    #with signal.NewQueue(8) as queue:
      log.debug(esc_08_Q)
      log.debug("Created esc_sn08__q_thread")
      thread_list.append(username)

      while True:
        log.debug("#08: Waiting for the queue data")
        try:
          data = esc_08_Q.get(True, 15) 
        except Queue.Empty:
          log.debug("#08: Queue empty")
        else:
          log.debug("Heart beat Rx for esc_sn08")
 

# o==================================o====================================o================================
# ESC SN 01
# o==================================o====================================o================================
def esc_sn01_handler(username):
    count = 0
    long(count)
    log.debug("Timer invoked esc_sn01_handler every 15sec")
    log.debug("Size of esc_sn01 queue %d" %(esc_01_Q.qsize()))
    if esc_01_Q.empty():
        log.debug("Queue 01 empty")
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn01, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(1, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            log.debug("Increment hbeat counter")
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        count = count + 1
        log.debug('Fetch data from esc_01_Q')
        esc_01_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        mysql.mysql_update_hb_count(count, username)
        snmp.snmp_set_operations(1, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_01_Q.task_done()
        heart_beat_counter = 0

#
def esc_sn01__q_thread(username):
    count = 0
    hb_counter = 0
    #with signal.NewQueue(1) as queue:
    log.debug(esc_01_Q)
    log.debug("Created esc_sn01__q_thread")
    thread_list.append(username)

    while True:
      log.debug("#01: Waiting for the queue data")
      try:
        data = esc_01_Q.get(True, 15) 
      except Queue.Empty:
        log.debug("#01: Queue empty")
        hb_counter = hb_counter + 1
        if hb_counter == 3:
          log.warn("No heart beat detected for esc_sn01, raise a trap")
          hb_counter = 0
      else:
        log.debug("Heart beat Rx for esc_sn01")
        count = count + 1
        #mysql.mysql_update_hb_count(count, username)
        #snmp.snmp_set_operations(1, "ACTIVE", "NA", 1, "ENABLE")
        esc_01_Q.task_done()
        hb_counter = 0



# o==================================o====================================o================================
# ESC SN 30
# o==================================o====================================o================================
def esc_sn030_handler(username):
    count = 0
    long(count)
    log.debug("Timer invoked esc_sn030_handler every 15sec")
    log.debug("Size of esc_sn030 queue %d" %(esc_030_Q.qsize()))
    if esc_030_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn030, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(1, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        count = count + 1
        log.debug('Fetch data from esc_030_Q')
        esc_030_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        mysql.mysql_update_hb_count(count, username)
        snmp.snmp_set_operations(1, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_030_Q.task_done()
        heart_beat_counter = 0

#
def esc_sn030__q_thread(username):
    log.debug("Created esc_sn30__q_thread")
    thread_list.append(username)
    while True:
        t2 = threading.Timer(15.0, esc_sn030_handler, args=(username,))
        t2.setName("esc_sn030__q_thread")
        t2.start() #after 15 seconds, trigger esc_sn030_handler
        time.sleep(15)
        t2.cancel()
# o==================================o====================================o================================
# ESC SN 10
# o==================================o====================================o================================
def esc_sn010_handler(username):
    count = 0
    long(count)
    log.debug("Timer invoked esc_sn010_handler every 15sec")
    log.debug("Size of esc_sn010 queue %d" %(esc_sn010_Q.qsize()))
    if esc_sn010_Q.empty():
        heart_beat_counter = heart_beat_dict[username]
        if heart_beat_counter == 3:
            log.warn("No heart beat detected for esc_sn010, raise a trap")
            #insert_query_to_hbeat_tbl(username, "DOWN", count, "IN-ACTIVE", "DISABLE", 1)
            snmp.snmp_set_operations(1, "IN-ACTIVE", "ARLINGTON", 1, "DISABLE")
            snmp_trap.trigger_trap("No heartbeat detected")
            heart_beat_dict[username] = 0
        else:
            heart_beat_counter = heart_beat_counter + 1
            heart_beat_dict[username] = heart_beat_counter
    else:
        count = count + 1
        log.debug('Fetch data from esc_sn010_Q')
        esc_sn010_Q.get()
        #insert_query_to_hbeat_tbl(username, "UP", count, "ACTIVE", "ENABLE", 1)
        mysql.mysql_update_hb_count(count, username)
        snmp.snmp_set_operations(1, "ACTIVE", "ARLINGTON", 1, "ENABLE")
        esc_sn010_Q.task_done()
        heart_beat_counter = 0

#
def esc_sn010__q_thread(username):
    log.debug("Created esc_sn10__q_thread")
    thread_list.append(username)
    while True:
        t2 = threading.Timer(15.0, esc_sn010_handler, args=(username,))
        t2.setName("esc_sn010__q_thread")
        t2.start() #after 15 seconds, trigger esc_sn010_handler
        time.sleep(15)
        t2.cancel()

