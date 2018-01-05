#!/bin/sh
iptables --flush
iptables -t nat --flush
#iptables -A INPUT -i tun+ -j ACCEPT
ps axf | grep monitor.py | grep -v grep | awk '{print "kill -9 " $1}' | sh
#ps axf | grep esc_main.py | grep -v grep | awk '{print "kill -9 " $1}' | sh
#ps axf | grep rest_server.py | grep -v grep | awk '{print "kill -9 " $1}' | sh

