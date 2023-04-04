# This file is executed on every boot (including wake-boot from deepsleep)
#import
#esp.osdebug(None)

import webrepl
import machine

WIFI_NAME = 'D-Link DSL-2750B'
WIFI_PASS = 'pegasus123'
def connect():
    from network import WLAN
    sta = WLAN()
    
    if machine.reset_cause() != machine.SOFT_RESET:
        sta.init(WLAN.STA)
        # configuration below MUST match your home router settings!!
        sta.ifconfig(config=('192.168.1.64', '255.255.255.0', '192.168.1.254', '8.8.8.8'))
        
    if not sta.isconnected():      
        nets = s.scan()
        for net in nets:
            if net.ssid == WIFI_NAME:
                print('Network found')
                sta.connect(net.ssid, auth=(net.sec, WIFI_PASS), timeout=5000)
                while not wlan.isconnected():
                   machine.idle() # save power while waiting
                print('WLAN connection succeeded!')
                print('network config:', sta_if.ifconfig())
                break
        else:
            print('Network not found!')
    
connect()
webrepl.start()