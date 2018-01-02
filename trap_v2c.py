#!/usr/bin/python
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntforg, context
from pysnmp.proto.api import v2c

import logmanager
log_m = logmanager.LogManager()
log = log_m.logger()
#1.3.6.1.4.1.8072.2.7.1.1.4.1.2.1 - sensorHealthTable, escID OID
def trigger_trap(temp):
	# Create SNMP engine instance
	snmpEngine = engine.SnmpEngine()

	# SecurityName <-> CommunityName mapping
	config.addV1System(snmpEngine, 'my-area', 'federated')

	# Specify security settings per SecurityName (SNMPv2c -> 1)
	config.addTargetParams(snmpEngine, 'my-creds', 'my-area', 'noAuthNoPriv', 1)

	# Setup transport endpoint and bind it with security settings yielding
	# a target name
	config.addSocketTransport(
	    snmpEngine,
	    udp.domainName,
	    udp.UdpSocketTransport().openClientMode()
	)
	config.addTargetAddr(
	    snmpEngine, 'my-nms',
	    udp.domainName, ('34.215.95.184', 162),
	    'my-creds',
	    tagList='all-my-managers'
	)

	# Specify what kind of notification should be sent (TRAP or INFORM),
	# to what targets (chosen by tag) and what filter should apply to
	# the set of targets (selected by tag)
	config.addNotificationTarget(
	    snmpEngine, 'my-notification', 'my-filter', 'all-my-managers', 'trap'
	)

	# Allow NOTIFY access to Agent's MIB by this SNMP model (2), securityLevel
	# and SecurityName
	config.addContext(snmpEngine, '')
	config.addVacmUser(snmpEngine, 2, 'my-area', 'noAuthNoPriv', (), (), (1,3,6))

	# *** SNMP engine configuration is complete by this line ***

	# Create default SNMP context where contextEngineId == SnmpEngineId
	snmpContext = context.SnmpContext(snmpEngine)

	# Create Notification Originator App instance.
	ntfOrg = ntforg.NotificationOriginator(snmpContext)

	# Build and submit notification message to dispatcher
	ntfOrg.sendNotification(
	    snmpEngine,
	    # Notification targets
	    'my-notification',
	    # Trap OID (SNMPv2-MIB::coldStart)
	    #(1,3,6,1,6,3,1,1,5,1),
            (1,3,6,1,4,1,8072,2,7,1,1,1,1,3,1),
	    # ( (oid, value), ... )
	    ( ((1,3,6,1,4,1,8072,2,7,1,1,1,1,3,1), v2c.OctetString(temp)),
            ((1,3,6,1,2,1,1,5,0), v2c.OctetString('Reason: esc app is down')) )
	)

	log.info('[SNMP-TRAP]Notification is scheduled to be sent')

	# Run I/O dispatcher which would send pending message and process response
	snmpEngine.transportDispatcher.runDispatcher()
