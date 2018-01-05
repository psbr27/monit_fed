#!/usr/bin/sh


systemctl stop openvpn@server.service
systemctl start openvpn@server.service
