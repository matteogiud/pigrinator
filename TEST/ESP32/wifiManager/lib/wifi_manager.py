import machine
from lib.wifiSecure import loadWifi, search
import network
import time
import uasyncio
from lib.microdot_asyncio import Microdot, Response, send_file, redirect
from lib.microdot_utemplate import render_template
#from lib.microdot import redirect

class WIFIManager:    
    
#     global __app
#     __app = Microdot()
    #Response.default_content_type = 'text/html'

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.AP = network.WLAN(network.AP_IF)
        self.AP.active(False)
        self.__app = Microdot()

    
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
        else:
            print('connected :', self.wlan.ifconfig())
            
            # not found any network
            
            
    def openAP(self):       
        
        self.AP.active(True)
        self.AP.config(essid="PIGRINATOR", password="pigrinator")
        while not self.AP.active():
            pass
        
        print('Connection successful')
        print(self.AP.ifconfig())        
            
        #define routing
        self.define_route()
                  
        
            
        try:
            self.__app.run(port=80)
        except:
            self.__app.shutdown()
            
            
    def define_route(self):
        @self.__app.get('/')
        def get_index_html(req):
            
            print("new request: ", str(req.client_addr))
            lst = []
            nets = self.wlan.scan()
            for (ssid, bssid, channel, RSSI, authmode, hidden) in nets:
                lst.append(ssid.decode('utf-8'))
            print(lst)
            # template = render_template('index.html', ssids = lst)
            # print(template)
            print(req.args)
            params = {'ssids': lst, 'err': (None if req.args.get('err') == None else req.args.get('err'))}
            return render_template('index.html', **params), 200, {'Content-Type': 'text/html'}
        
        @self.__app.post('/')
        def post_try_connection(req):
            print(str(req.form))
            
            ssid=req.form.get('ssid')
            psw=req.form.get('psw')
            save_wifi=True if req.form.get('saveWifi') == "true" else False
            if(self.tryConnection(ssid, psw, save_wifi)):                
                return """<html>
                                <body>
                                    <h1>Connected to wifi!!</h1>
                                </body>
                            </html>""", 200, {'Content-Type': 'text/html'}
                self.AP.active(False)
            else:
                return redirect('/?err=impossible to connect')
            
            
        
    def tryConnection(self, SSID, PSW, save_connection = False):
        self.wlan.connect(SSID, PSW)
        t = time.ticks_ms()
        while not self.wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t) > 5000:
                self.wlan.disconnect()
                print("Timeout. Could not connect.")
                return False
        if self.wlan.isconnected():
            print("Connected to wifi " + SSID)
            if save_connection:
                loadWifi(SSID, PSW)
                print('Connection saved')                
            return True
        else:
            try:
                self.wlan.disconnect()
            except:
                pass
            print("Cannot connect to wifi")
            return False
