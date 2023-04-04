from machine import Pin, PWM
from lib.motorsDriver import MotorsDriver
import uasyncio
from lib.microdot_asyncio import Microdot

MD = MotorsDriver(Pin(27, Pin.OUT), Pin(14, Pin.OUT), Pin(33, Pin.OUT), Pin(32, Pin.OUT), PWM(Pin(26, Pin.OUT)), PWM(Pin(25, Pin.OUT)),1000)
MD.stop()

#setup webserver
app = Microdot()

@app.route('/')
def hello(request):
    return 'Hello World'

@app.route('/forward')
def forward(request):
    MD.forward()
    return 'Car is forward'

@app.route('/backward')
def backward(request):
    MD.forward()
    return 'Car is backward'

@app.route('/stop')
def backward(request):
    MD.stop()
    return 'Car is stopped'

def start_server():
    print('starting server...')
    try:
        app.run(port=80)
    except:
        app.shutdown()
