import time
import network
import uasyncio as asyncio
from lib.microdot_asyncio import Microdot, Response, send_file, redirect
from lib.microdot_utemplate import render_template
import urequests
from lib.wifi_manager import WIFIManager
import global_vars
import json
import lib.paths_handler as path
from machine import Pin



# wifiManager = WIFIManager()
# wifiManager.connect()


# setup webserver
print(f"[main] car ip: [{global_vars.esp_car_ip_address}]")

app = Microdot()

pump = Pin(23, Pin.OUT)
pump.off()

trigger_pin = Pin(12, Pin.OUT)
echo_pin = Pin(14, Pin.IN)

def check_glass_position():
    
    
    
    for i in range(10):
        trigger_pin.value(1)
        time.sleep_us(10)
        trigger_pin.value(0)
    
         # Attendi il segnale di echo
        while echo_pin.value() == 0:
            pass
        start_time = time.ticks_us()
        
        while echo_pin.value() == 1:
            pass
        end_time = time.ticks_us()
        
        # Calcola la durata dell'eco
        durata = end_time - start_time
        
        # Calcola la distanza in base alla durata
        distanza = durata * 0.0343 / 2
        print("distanza misurata: ", distanza)
        
        if distanza > 20:
            return False
        
    return True



@app.get('/searchAllPaths')
def searchAllPath(req):
    paths = path.search_all()
    return paths, 200, {"Content-Type": "application/json"}

@app.put('/newPath')
def newPath(req):
    json_body = json.loads(req.body.decode('utf-8'))
    print(f"[/newPath] new request: {req.body}")        
    
    if not json_body["path"]:        
        return "bad request, syntax error", 400, {"Content-Type": "text/html"}
    
    path_id_created = path.loadPath(json_body["path"])
    if path_id_created == -1 or path_id_created is None:
        return "bad request, syntax error", 400, {"Content-Type": "text/html"}
    
    return {"path_id": path_id_created}, 201, {"Content-Type": "application/json"}

@app.get('/searchPath/<int:path_id>')
def searchPath(req, path_id):
    # json_body = json.loads(req.body.decode('utf-8'))
    print(f"[/searchPath] new request, path_id: {path_id}")        
    
    if not path_id:        
        return "bad request, syntax error", 400, {"Content-Type": "text/html"}
    
    path_found = path.search(path_id)
    if not path_found:
        return "bad request, syntax error", 400, {"Content-Type": "text/html"}
    
    return path_found, 200, {"Content-Type": "application/json"}

@app.get('/loadWater')
def loadWater(req):
    print("/loadWater")
    if check_glass_position():
        try:
            pump.on()
            time.sleep(2)
            pump.off()
        except:
            pump.off()
        return 'OK'
    else:
        return 'ERROR'


@app.post('/goTo')
def goTo(req):
    print("[/goTo]body: ", req.body)
    
    json_body = json.loads(req.body.decode('utf-8'))

    path_id = json_body["path_id"]
    complete_path = path.search(path_id)  # risolvere: ritorna null
    if complete_path is None:
        return "bad request", 400, {"Content-Type": "text/html"}
    print(f"[\goTo]: selected path: {complete_path}")
    # risolvere: prendere ip inviato durante la connessione
    car_http_req = f"http://{global_vars.esp_car_ip_address}/followThisPath"
    # car_http_req = f"http://192.168.1.60/followThisPath"
    # print(car_http_req)
    try:
        response = urequests.post(car_http_req, headers={
                                  "Content-Type": "application/json"}, data=json.dumps(complete_path))
        if response.status_code == 200:  # solleva un'eccezione se la risposta ha uno stato HTTP diverso da 2XX
            print(f"[\goTo]: response status code: {response.status_code}")
            return 'ok', 200, {"Content-Type": "text/html"}
        else:
            return 'Car is not ready', 503, {"Content-Type": "text/html"}

    except Exception as e:
        print("Errore HTTP:", e)
        # print("Risposta HTTP:", response.text)
        return 'Car is not ready', 503, {"Content-Type": "text/html"}

    return 'Car is not ready', 503, {"Content-Type": "text/html"}


@app.get('/')
def index(req):
    return 'hello'

def start_server():
    try:
        # debug=True,
        app.run(port=80)
    except:
        app.shutdown()


start_server()
