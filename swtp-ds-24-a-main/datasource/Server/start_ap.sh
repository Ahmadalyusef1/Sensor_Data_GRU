#!/bin/bash

nmcli dev wifi hotspot ifname wlan1 ssid jetson0x password "Alea iacta est!"
nmcli dev wifi show-password
