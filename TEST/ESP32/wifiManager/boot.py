from lib.wifi_manager import WIFIManager
from machine import Pin
from time import sleep_ms
import lib.global_vars as g

g.init()

wifiManager = WIFIManager()


led = Pin(2, Pin.OUT)
led.on()
sleep_ms(300)
led.off()
sleep_ms(300)
led.on()
sleep_ms(300)
led.off()


wifiManager.connect()
#('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
