#!/bin/bash

# Use a web service to get public IP address
ip_address=$(curl -s https://api.ipify.org)

#Fixing Squid proxy

sudo apt update
sudo apt install squid
sudo systemctl start squid
sudo systemctl enable squid
sudo systemctl restart squid

sleep 1

cat << SQ > /etc/squid/squid.conf
# BonvScripts
# https://t.me/BonvScripts
# Please star my Repository: https://github.com/Bonveio/BonvScripts
# https://phcorner.net/threads/739298

acl VPN dst $ip_address/32
http_access allow VPN
http_access deny all
http_port 0.0.0.0:8000
http_port 0.0.0.0:8080
acl bonv src 0.0.0.0/0.0.0.0
no_cache deny bonv
dns_nameservers 1.1.1.1 1.0.0.1
visible_hostname localhost
SQ

sleep 2
dos2unix -q /etc/squid/squid.conf
service squid restart

#SSL PORT FIXER
sudo systemctl start stunnel4 
sudo systemctl enable stunnel4 
sudo systemctl restart stunnel4 

#Restarting Ssh 
sudo systemctl start ssh
sudo systemctl enable ssh
sudo systemctl restart ssh

#Restarting Dropbear
sudo systemctl start dropbear
sudo systemctl enable dropbear
sudo systemctl restart dropbear

sleep 2
# Fixing Ovpn Port
bash -c "sed -i "/ncp-disable/d" /etc/openvpn/server/*.conf;systemctl restart openvpn-server@{ec_s,s}erver_{tc,ud}p"

sleep 2s
sudo systemctl start openvpn
sudo systemctl enable openvpn
sudo systemctl restart openvpn
systemctl daemon-reload
    
echo "SSL /OVPN / PROXY PORT FIXED"
echo "YOUR WELCOME"
