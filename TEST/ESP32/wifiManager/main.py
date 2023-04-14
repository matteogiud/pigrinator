from machine import Pin, PWM
import time
import network
import uasyncio as asyncio
from lib.microdot_asyncio import Microdot, Response, send_file, redirect
from lib.microdot_utemplate import render_template
from lib.motor_driver import MotorsDriver

MD = MotorsDriver(Pin(27, Pin.OUT), Pin(14, Pin.OUT), Pin(33, Pin.OUT), Pin(32, Pin.OUT), PWM(Pin(26, Pin.OUT)), PWM(Pin(25, Pin.OUT)),1000)
MD.stop()

print(network.WLAN(network.STA_IF).ifconfig())

#setup webserver
app = Microdot()

@app.route('/')
def hello(request):
    return 'Hello World'

@app.route('/forward')
def forward(request):
    MD.forward()
    return 'OK', 200

@app.route('/backward')
def backward(request):
    MD.forward()
    return 'OK', 200

@app.route('/right')
def backward(request):
    MD.right()
    return 'OK', 200

@app.route('/left')
def backward(request):
    MD.left()
    return 'OK', 200

@app.route('/stop')
def backward(request):
    MD.stop()
    return 'OK', 200

def start_server():    
    try:
        app.run(debug=True, port=80)
    except:
        app.shutdown()
        
        
start_server()

