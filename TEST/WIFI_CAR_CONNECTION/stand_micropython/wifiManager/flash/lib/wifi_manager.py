import machine
from lib.wifiSecure import loadWifi, search
import network
import time
import uasyncio
from lib.microdot_asyncio import Microdot, Response, redirect
from lib.microdot_utemplate import render_template
import _thread


class WIFIManager:    
    
#     global __app
#     __app = Microdot()
    #Response.default_content_type = 'text/html'

    def __init__(self):
        self.led_status = machine.Pin(2, machine.Pin.OUT)
        self.led_status.off()
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.AP = network.WLAN(network.AP_IF)
        self.AP.active(False)
        self.__app = Microdot()
        self.wifi_credential = {"ssid": None, "psw": None}
        self.openAP()

    
    def addWifiSetting(self, SSID, PSW):
        loadWifi(SSID, PSW)
        
    def connect(self, wifi_settings=None) -> network.WLAN:
         

        self.wifi_settings=wifi_settings
        if not self.wlan.isconnected():
            nets = self.wlan.scan()
            for (ssid, bssid, channel, RSSI, authmode, hidden) in nets:
                print(ssid.decode("utf-8"))
                pswFound = search(ssid.decode("utf-8"))
                if pswFound != None:
                    if self.tryConnection(ssid.decode("utf-8"), pswFound):
                        self.led_status.on()                        
                        return self.wlan           
            print("Net not found")
            self.openAP()
            self.led_status.off()
        else:
            if not self.wifi_settings is None:
                self.wlan.ifconfig(wifi_settings)
            print('Connected :', self.wlan.ifconfig())
            self.led_status.on()
            
            # not found any network
            
            
    def openAP(self):               
        
        self.AP.active(True)
        self.AP.config(essid="PIGRINATOR", password="pigrinator")
        while not self.AP.active():
            pass
        
        print('AP on ')
        print(self.AP.ifconfig())        
            
        #define routing
        self.define_route()
                  
        
        def run_server():
            try:
                self.__app.run(port=80)
            except:
                self.__app.shutdown()
            self.AP.active(False)
            print('AP off')
                
        _thread.start_new_thread(run_server, ())
        
            
            
    def define_route(self):
       
        @self.__app.get('/')
        def get_index_html(req):
            
            print("new request: ", str(req.client_addr))
            lst = []
            nets = self.wlan.scan()
            for (ssid, bssid, channel, RSSI, authmode, hidden) in nets:
                lst.append(ssid.decode('utf-8'))
            print(lst)
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
                # req.app.shutdown()
                return """<html>
                                <body align='center'>
                                    <h1>Connected to wifi!!</h1>
                                </body>
                            </html>""", 200, {'Content-Type': 'text/html'}
                
            else:
                return redirect('/?err=impossible to connect')
            
        @self.__app.get('/shutdown')
        def shutdown(request):
            request.app.shutdown()
            return 'The server is shutting down...'


        @self.__app.post('/getWifiCredential')
        def getWifiCredential(req):
            import json; json_body=json.loads(req.body.decode('utf-8'))
            
            if json_body["mac_address"] != "C8:F0:9E:53:14:EC":
                return "forbidden", 403, {'Content-Type': 'text/html'}
            if not self.wifi_credential["ssid"] is None and not self.wifi_credential["psw"] is None:
                if self.wlan.isconnected():
                    return self.wifi_credential, 200, {'Content-Type': 'application/json'}
                
            return {"notAlreadyConnected": True}, 503, {'Content-Type': 'application/json'}
            
            
        
    def tryConnection(self, SSID, PSW, save_connection = False):
        self.wlan.connect(SSID, PSW)
        t = time.ticks_ms()
        while not self.wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t) > 5000:
                self.wlan.disconnect()
                print("Timeout. Could not connect.")
                self.led_status.off()
                return False
        if self.wlan.isconnected():
            if not self.wifi_settings is None:
                self.wlan.ifconfig(self.wifi_settings)
            print("Connected to wifi ", SSID , self.wlan.ifconfig())
            if save_connection:
                loadWifi(SSID, PSW)
                print('Connection saved')
                self.wifi_credential["ssid"] = SSID
                self.wifi_credential["psw"] = PSW
                self.led_status.on()
                
            return True
        else:
            try:
                self.wlan.disconnect()
            except:
                pass
            print("Cannot connect to wifi")
            self.led_status.off()
            return False

