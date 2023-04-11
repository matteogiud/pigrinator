import machine
from lib.wifiSecure import loadWifi, search
import network
import time
import uasyncio
from lib.microdot_asyncio import Microdot, Response, send_file
from lib.microdot_utemplate import render_template

class WIFIManager:
    
    
    global __app
    __app = Microdot()
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.AP = network.WLAN(network.AP_IF)
        self.AP.active(False)

    
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
            self.openAP()
            
            # not found any network
            
            
    def openAP(self):       
        
        self.AP.active(True)
        self.AP.config(essid="MicroPython-AP", password="esp")
        while self.AP.active() == False:
            pass
        
        print('Connection successful')
        print(self.AP.ifconfig())
        try:
            __app.run(port=80)
        except:
            __app.shutdown()
            
            
    @__app.route('/')
    def web_page(request):
        return "hello world"

          
                    
                    
                    
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
            try:
                self.wlan.disconnect()
            except:
                pass
            print("Cannot connect to wifi")
            return False
        
    
            
        
        
                    
                    
        
        
    
    
        
        
