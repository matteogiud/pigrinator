import machine
from lib.wifiSecure import loadWifi, search
import network
import time
import uasyncio
from lib.microdot_asyncio import Microdot, Response, redirect
from lib.microdot_utemplate import render_template
import _thread
import global_vars



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
        self.wifi_credential = {"ssid": None, "psw": None, "myIp": None}
        self.car_robot_connected = False #indica se il robot si è collegato alla rete oppure no
        self.mdns_hostname = "pigrinatorstand"

    
    def addWifiSetting(self, SSID, PSW):
        loadWifi(SSID, PSW)
        
    def connect(self, wifi_settings=None) -> network.WLAN:         
        if not self.AP.active():#se non è attivo l'ap lo accende
            self.openAP()
        self.wifi_settings=wifi_settings
        if not self.wlan.isconnected():
            nets = self.wlan.scan()
            for (ssid, bssid, channel, RSSI, authmode, hidden) in nets:
                print(ssid.decode("utf-8"))
                pswFound = search(ssid.decode("utf-8"))
                if pswFound != None:
                    if self.tryConnection(ssid.decode("utf-8"), pswFound):
                        # self.led_status.on()                        
                        return self.wlan           
            print("Net not found")
            #  self.openAP()
            self.led_status.off()
        else:
            if not self.wifi_settings is None:
                self.wlan.ifconfig(wifi_settings)
            ssid = self.wlan.config("essid")
            print(ssid)
            psw = search(ssid)
            if psw is None:
                self.wlan.disconnect()
                machine.restart()                    
            self.wifi_credential["ssid"]=ssid 
            self.wifi_credential["psw"] = psw
            self.wifi_credential["myIp"] = self.wlan.ifconfig()[0]
            
            print(f'Connected to {self.wifi_credential["ssid"]}:', self.wlan.ifconfig())
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
                  
        
        
        _thread.stack_size(8192)  # impostare la dimensione dello stack a 8192 byte
        _thread.start_new_thread(self.__run_server, ())
        print("server started")
        
    def __run_server(self):
        
        try:
            self.__app.run(port=80)
        except:
            self.__app.shutdown()
        self.AP.active(False)
        print('AP off')   
            
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
            
        @self.__app.post('/shutdown')
        def shutdown(req):
            import json; json_body=json.loads(req.body.decode('utf-8'))            

            if json_body["mac_address"] != "C8:F0:9E:53:14:EC": #autorizza la richiesta
                return "forbidden", 403, {'Content-Type': 'text/html'}
            
            @req.after_request
            def shutdown(req, res):
                print("waiting to esp car connecting")
#                 check_esp_car_connection_timer = machine.Timer(0)
#                 check_esp_car_connection_timer.init(period=5000, mode=machine.Timer.ONE_SHOT, callback=self.check_esp_car_connection)
                time.sleep(5)
                self.check_esp_car_connection()
                if self.car_robot_connected:
                    req.app.shutdown()
                else:
                    print("robot not already connected")
                print("robot connected")
                return 'The server is shutting down...'


            print("ip: ", json_body["actual_ip_address"])
            global_vars.esp_car_mdns_hostname = json_body["actual_ip_address"]
            print(f"[shutdown request] ip saved: {global_vars.esp_car_mdns_hostname}")
            # self.car_robot_connected = True
            print("AP shutting down...")
            
            
            
            return 'The server is shutting down...'

    
        @self.__app.post('/getWifiCredential')
        def getWifiCredential(req):
            import json; json_body=json.loads(req.body.decode('utf-8'))
            if json_body["mac_address"] != "C8:F0:9E:53:14:EC":
                return "forbidden", 403, {'Content-Type': 'text/html'}
            print(self.wifi_credential)
            if not self.wifi_credential["ssid"] is None and not self.wifi_credential["psw"] is None and not self.wifi_credential["myIp"] is None:
                if self.wlan.isconnected():
                    return self.wifi_credential, 200, {'Content-Type': 'application/json'}
                
            return {"notAlreadyConnected": True}, 503, {'Content-Type': 'application/json'}
            
    
    def check_esp_car_connection(self):
        import urequests
        import json
        import utils
        
        
        esp_car_ip = utils.get_ip_from_mdns(global_vars.esp_car_mdns_hostname) # mi trova l'ip dell'esp32
        # http_esp_car_request = f"http://{esp_car_ip}/"
        print(f"ip: {esp_car_ip}")
        if esp_car_ip is None: # se non è stato trovato l'ip allora setto che il robot non è pronto
            self.car_robot_connected = False
            return
        http_esp_car_request = f"http://{esp_car_ip}/"
        time_to_try = 5
        while time_to_try > 0:
            time.sleep(1)
            try:
                response = urequests.get(url = http_esp_car_request)
                if response.status_code == 200:
                    self.car_robot_connected = True
                    self.car_robot_ip_address = esp_car_ip
                    print("car is connected")
                    break                
            except Exception as e:
                print(f"ex: {e}")
                self.car_robot_connected = False
            time_to_try-=1
                
        
        
    
    def tryConnection(self, SSID, PSW, save_connection = False):        
        self.wlan.config(dhcp_hostname = self.mdns_hostname) # mdns configure
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
            host = self.wlan.config('dhcp_hostname') 
            print("Connected to wifi ", SSID , self.wlan.ifconfig(), "hostname:", host)
            if save_connection:
                loadWifi(SSID, PSW)
                print('Connection saved')
            self.wifi_credential["ssid"] = SSID
            self.wifi_credential["psw"] = PSW
            self.wifi_credential["myIp"] = self.wlan.ifconfig()[0]
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

