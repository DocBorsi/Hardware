#!/bin/bash

# Script to set up an open Wi-Fi hotspot on Raspberry Pi

# Variables
SSID="BoteCannected"  # Set your desired SSID
INTERFACE="wlan0"       # Wireless interface
STATIC_IP="192.168.4.1" # Static IP for the hotspot
DHCP_RANGE="192.168.4.2,192.168.4.20,255.255.255.0,24h"

# Update and install required packages
echo "Updating system and installing required packages..."
apt update && apt upgrade -y
apt install -y dnsmasq hostapd

# Configure static IP
echo "Configuring static IP..."
cat <<EOL >> /etc/dhcpcd.conf
interface $INTERFACE
    static ip_address=$STATIC_IP/24
    nohook wpa_supplicant
EOL

# Configure dnsmasq
echo "Configuring dnsmasq..."
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cat <<EOL >> /etc/dnsmasq.conf
interface=$INTERFACE       # Use the wireless interface
dhcp-range=$DHCP_RANGE
EOL

# Configure hostapd for open network
echo "Configuring hostapd..."
cat <<EOL >> /etc/hostapd/hostapd.conf
interface=$INTERFACE
driver=nl80211
ssid=$SSID
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=0                      # Set to 0 for an open network
EOL

# Point hostapd to the configuration file
echo "Pointing hostapd to the configuration file..."
echo "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"" >> /etc/default/hostapd

# Enable IP forwarding
echo "Enabling IP forwarding..."
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p

# Set up NAT with iptables
echo "Setting up NAT with iptables..."
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Enable hostapd and dnsmasq on boot
echo "Enabling services to start on boot..."
systemctl enable hostapd
systemctl enable dnsmasq

# Restart services
echo "Restarting services..."
systemctl restart dnsmasq
systemctl restart hostapd

# Completion message
echo "Open hotspot setup completed. You can connect using SSID: $SSID"

# Optional: Show iptables rules (for checking)
echo "Current iptables rules:"
iptables -L -v
