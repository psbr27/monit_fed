#!/usr/bin/sh

iptables --flush
iptables -t nat --flush
# Allow TUN interface connections to OpenVPN server
iptables -A INPUT -i tun+ -j ACCEPT

# Allow TUN interface connections to be forwarded through other interfaces
#iptables -A FORWARD -i tun+ -j ACCEPT

systemctl stop openvpn@server.service
systemctl start openvpn@server.service
