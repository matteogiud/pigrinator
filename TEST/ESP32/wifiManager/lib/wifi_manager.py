import machine
from lib.wifiSecure import loadWifi, search
import network
import time

class WIFIManager:    
    
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
    
    def addWifiSetting(self, SSID, PSW):
        loadWifi(SSID, PSW)
        
    def connect(self) -> network.WLAN:
        if not self.wlan.isconnected():
            nets = self.wlan.scan()
            for (ssid, bssid, channel, RSSI, authmode, hidden) in nets:
                print(ssid.decode("utf-8"))
                pswFound = search(ssid.decode("utf-8"))
                if pswFound != None:
                    if self.tryConnection(ssid.decode("utf-8"), pswFound):
                        return self.wlan           
            print("Net not found")
            # not found any network
                    
                    
                    
    def tryConnection(self, SSID, PSW):
        self.wlan.connect(SSID, PSW)
        t = time.ticks_ms()
        while not self.wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t) > 5000:
                self.wlan.disconnect()
                print("Timeout. Could not connect.")
                return False
        if self.wlan.isconnected():
            print("Connected to wifi " + SSID)
            return True
        else:
            print("Cannot connect to wifi")
            return False
            
        
        
                    
                    
        
        
    
    
        
        
