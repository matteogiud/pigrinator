import time
import network
import uasyncio as asyncio
from lib.microdot_asyncio import Microdot, Response, send_file, redirect
from lib.microdot_utemplate import render_template
import urequests
from lib.wifi_manager import WIFIManager
import lib.global_vars as global_vars



# wifiManager = WIFIManager()
# wifiManager.connect()


#setup webserver
print(f"car ip: [{global_vars.esp_car_ip_address}]")

app = Microdot()

@app.post('/goTo')
def goTo(req):
    print("body: ", req.body)
    import json; json_body=json.loads(req.body.decode('utf-8'))
    
    import lib.paths_handler as paths
    path_id = json_body["path_id"]
    complete_path = paths.search(path_id) #risolvere: ritorna null
    if complete_path is None:
        return "bad request", 400, {"Content-Type": "text/html"}
    print(f"[\goTo]: selected path: {complete_path}")
    # car_http_req = f"http://{global_vars.my_vars['esp_car_ip_address']}/followThisPath" #risolvere: prendere ip inviato durante la connessione
    car_http_req = f"http://192.168.1.60/followThisPath"
    # print(car_http_req)
    try:
        response = urequests.post(car_http_req, headers={"Content-Type": "application/json"}, data=json.dumps(complete_path))
        if response.status_code == 200: # solleva un'eccezione se la risposta ha uno stato HTTP diverso da 2XX
            print(f"[\goTo]: response status code: {response.status_code}")
            return 'ok', 200, {"Content-Type": "text/html"}
        else:
            return 'Car is not ready', 503 , {"Content-Type": "text/html"}

    except Exception as e:
        print("Errore HTTP:", e)
        # print("Risposta HTTP:", response.text)
        return 'Car is not ready', 503 , {"Content-Type": "text/html"}

    
    
    return 'Car is not ready', 503 , {"Content-Type": "text/html"}
    
    
@app.get('/')
def index(req):
    return 'hello'

def start_server():
    try:
        #debug=True, 
        app.run(port=80)
    except:
        app.shutdown()
        

start_server()


