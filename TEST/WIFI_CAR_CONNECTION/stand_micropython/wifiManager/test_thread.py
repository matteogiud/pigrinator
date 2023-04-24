import _thread
from microdot import Microdot
import network

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="pippo", password="")

app = Microdot()

# Definisci la tua route qui
@app.route('/', methods=['GET'])
def handle_example(request):
    return "hello"

def run_server():
    # Imposta l'access point qui
    app.run(host='192.168.4.1', port=80)

# Avvia il thread del server web
_thread.start_new_thread(run_server, ())

for i in range(10):
    print("ciao")