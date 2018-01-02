#!/usr/bin/python

import pickle
import socket
import sys
import threading
import time

import simplejson as json

import dynamodblib
import logmanager
import trap_v2c as snmpA
import esc_queue as esc_q

log_m = logmanager.LogManager()
log = log_m.logger()

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

dyanmo_db = dynamodblib.DynamoDB()
healthDB = dynamodblib.sensorHealthDB()
siteID_list = []
create_flag = 1

cmdGen = cmdgen.CommandGenerator()


# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

def set_d_b_str(entry, value):
    error_indication, error_status, error_index, var_binds = cmdGen.setCmd(
        cmdgen.CommunityData('federated'),
        cmdgen.UdpTransportTarget(('34.215.95.184', 161)), (entry, rfc1902.OctetString(value)), )
    # Check for errors and print out results
    if error_indication:
        log.error(error_indication)
    else:
        if error_status:
            log.debug('%s at %s' % (error_status.prettyPrint(), error_index and var_binds[int(error_index) - 1] or '?'))
        else:
            for name, val in var_binds:
                log.debug('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


#
def set_d_b_int(entry, value):
    error_indication, error_status, error_index, var_binds = cmdGen.setCmd(
        cmdgen.CommunityData('federated'),
        cmdgen.UdpTransportTarget(('34.215.95.184', 161)), (entry, rfc1902.Integer(value)), )
    # Check for errors and print out results
    if error_indication:
        log.error(error_indication)
    else:
        if error_status:
            log.debug('%s at %s' % (error_status.prettyPrint(), error_index and var_binds[int(error_index) - 1] or '?'))
        else:
            for name, val in var_binds:
                log.debug('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# unsigned handler
def set_d_b_unsigned(entry, value):
    error_indication, error_status, error_index, var_binds = cmdGen.setCmd(
        cmdgen.CommunityData('federated'),
        cmdgen.UdpTransportTarget(('34.215.95.184', 161)), (entry, rfc1902.Counter64(value)), )
    # Check for errors and print out results
    if error_indication:
        log.error(error_indication)
    else:
        if error_status:
            log.debug('%s at %s' % (error_status.prettyPrint(), error_index and var_binds[int(error_index) - 1] or '?'))
        else:
            for name, val in var_binds:
                log.debug('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# snmpset -v2c -c federated 34.215.95.184 1.3.6.1.4.1.8072.2.7.1.1.4.1.2.1 s "FL033C"
# esIndex         escID channelId detectionFlag timeStampSensorResults maxRssiDbm minRssiDbm maxSnrDb minSnrDb numDetections numAttempts numDetectionsTimeWindow numAttemptsTimeWindow probDetection probDetectionTimeWindow
stats = "1.3.6.1.4.1.8072.2.7.1.1.3.1."
operational = "1.3.6.1.4.1.8072.2.7.1.1.1.1."

""" Function: Operation state """


def snmp_set_operations(escId, opState, siteId, entry, adminState):
    set_d_b_int((operational + str(1) + "." + str(entry)), escId)
    set_d_b_str((operational + str(2) + "." + str(entry)), siteId)
    set_d_b_str((operational + str(3) + "." + str(entry)), opState)
    set_d_b_str((operational + str(4) + "." + str(entry)), adminState)


""" Function: Thread_2 handle csv file handler requests """


def csv_client_handler(connection, e, t):
    while True:
        while not e.isSet():
            log.debug('wait for event timeout')
            event_is_set = e.wait()
            if event_is_set:
                log.debug("Sync sent to CSV app")
                data = connection.send("Sync")
            else:
                log.debug('do nothing')
        time.sleep(2)


""" Function: Thread_1 handle rest server requests """


def snmp_handler_response(sock, Q3):
    global create_flag
    index_counter = 0
    while True:
        log.debug("[snmp_handler_response] waiting for rest server data..")
        data = Q3.get(True)
        if data:
            json_parse = json.loads(data)
            #json_file = open("health_data.json", 'w')
            #pickle.dump(json_parse, json_file)
            #json_file.close()
            band_id = json_parse['bandIndex']
            entry = band_id
            esc_id = json_parse['sensorId']
            log.debug("[%s] Heart beat Rx" %(esc_id))
            # retrieve sensor Id fed_esc_029 to esc_sn029
            log.debug("[%s] send data client manager" % esc_id)
            #Push it to client heart beat manager
            sock.send(data)

            if (band_id == 0 or band_id == 1) and index_counter < 6:
                log.debug("---> Window Stared <---")
                if create_flag == 1:
                    for num in xrange(1, 7):
                        siteId = esc_id + "_" + str(num)
                        siteID_list.append(siteId)
                        healthDB.createItem(siteId)
                    create_flag = 0
                else:
                    print("")

            if index_counter == 6:
                log.debug("reset counter to zero")
                index_counter = 0

            band_info = json_parse['bandInfo']['timeStampHealthCheck']
            sensor = json_parse['bandInfo']['sensor']
            adi_settings = json_parse['bandInfo']['adiSettings']
            hps = json_parse['hps']
            i2c = json_parse['i2c']

            set_d_b_str((stats + str(2) + "." + str(entry)), esc_id)
            set_d_b_int((stats + str(3) + "." + str(entry)), band_id)
            set_d_b_int((stats + str(4) + "." + str(entry)), band_info)
            set_d_b_int((stats + str(5) + "." + str(entry)), sensor['agcGain'])
            set_d_b_int((stats + str(6) + "." + str(entry)), sensor['gpioOverLoad'])
            set_d_b_int((stats + str(7) + "." + str(entry)), sensor['gpioSPIvalue'])
            set_d_b_str((stats + str(8) + "." + str(entry)), sensor['rmsAverage'])
            set_d_b_int((stats + str(9) + "." + str(entry)), sensor['agcMaxVal'])
            set_d_b_str((stats + str(10) + "." + str(entry)), sensor['noiseRssiDbm'])
            set_d_b_int((stats + str(11) + "." + str(entry)), sensor['dcI'])
            set_d_b_int((stats + str(12) + "." + str(entry)), sensor['dcQ'])
            set_d_b_int((stats + str(13) + "." + str(entry)), sensor['iqImbalanceGaindB'])
            set_d_b_int((stats + str(14) + "." + str(entry)), sensor['iqImbalancePhaseDeg'])
            set_d_b_int((stats + str(15) + "." + str(entry)), sensor['numDmaOverflows'])
            set_d_b_unsigned((stats + str(16) + "." + str(entry)), adi_settings['adiRxLoHz'])
            set_d_b_unsigned((stats + str(17) + "." + str(entry)), adi_settings['adiTxLoHz'])
            set_d_b_int((stats + str(18) + "." + str(entry)), adi_settings['adiGainValue'])
            set_d_b_int((stats + str(19) + "." + str(entry)), adi_settings['adiTxAttenutation'])
            set_d_b_unsigned((stats + str(20) + "." + str(entry)), adi_settings['adiRxClockHz'])
            set_d_b_unsigned((stats + str(21) + "." + str(entry)), adi_settings['adiTxClockHz'])
            set_d_b_int((stats + str(22) + "." + str(entry)), hps['oneMinLoad'])
            set_d_b_int((stats + str(23) + "." + str(entry)), hps['memoryFreeKb'])
            set_d_b_int((stats + str(24) + "." + str(entry)), hps['memoryTotalKb'])
            set_d_b_int((stats + str(25) + "." + str(entry)), hps['upTime'])
            set_d_b_int((stats + str(26) + "." + str(entry)), hps['cpuClockSpeed'])
            set_d_b_str((stats + str(27) + "." + str(entry)), i2c['humidity'])
            set_d_b_str((stats + str(28) + "." + str(entry)), i2c['temperature'])
            set_d_b_int((stats + str(29) + "." + str(entry)), i2c['compass_x_axis'])
            set_d_b_int((stats + str(30) + "." + str(entry)), i2c['compass_y_axis'])
            set_d_b_int((stats + str(31) + "." + str(entry)), i2c['compass_z_axis'])
            set_d_b_int((stats + str(32) + "." + str(entry)), i2c['compassChange'])
            # set the signal to false
            # e.clear()
            if(i2c['temperature'] > 120):
              snmpA.trigger_trap(str(i2c['temperature']))
            if(i2c['compassChange'] == 1):
              snmpA.trigger_trap(str(i2c['compassChange']))
            healthDB.setItem(siteID_list[index_counter], band_id, str(band_info), sensor['agcGain'], sensor['gpioOverLoad'],
                             sensor['gpioSPIvalue'], str(sensor['rmsAverage']), sensor['agcMaxVal'],
                             str(sensor['noiseRssiDbm']), sensor['dcI'], sensor['dcQ'], sensor['iqImbalanceGaindB'],
                             sensor['iqImbalancePhaseDeg'], sensor['numDmaOverflows'], adi_settings['adiRxLoHz'],
                             adi_settings['adiTxLoHz'], adi_settings['adiGainValue'], adi_settings['adiTxAttenutation'],
                             adi_settings['adiRxClockHz'], adi_settings['adiTxClockHz'], hps['oneMinLoad'],
                             hps['memoryFreeKb'], hps['memoryTotalKb'], hps['upTime'], hps['cpuClockSpeed'],
                             str(i2c['humidity']), str(i2c['temperature']), i2c['compass_x_axis'], i2c['compass_y_axis'],
                             i2c['compass_z_axis'], i2c['compassChange'])
            index_counter = index_counter + 1


def create_socket():
    # create a TCP/IP socket
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def rest_connections(Q, port_no):
    log.debug("+++ snmp stat handler (P3) +++")
    time.sleep(3)
    server_addr = ('localhost', port_no)
    sock = create_socket()
    while True:
      try:
        sock.connect(server_addr)
        break
      except ValueError:
        log.debug("Connection error in rest_connections handler.. keep re-trying")
        continue

    snmp_handler_response(sock, Q)
