#from lib.wifi_manager import WIFIManager
from machine import Pin
from time import sleep_ms
import global_vars
from wifi_manager import WIFIManager

global_vars.init() #inizializzo le variabili globali

wifiManager = WIFIManager()


led = Pin(2, Pin.OUT)
led.on()
sleep_ms(300)
led.off()
sleep_ms(300)
led.on()
sleep_ms(300)
led.off()

print("Is Connecting...")
wifiManager.connect()
while not wifiManager.car_robot_connected:
    pass
print (f"[boot] mdns car before setting: {global_vars.esp_car_mdns_hostname}")
global_vars.esp_car_ip_address = wifiManager.car_robot_ip_address
print (f"[boot] ip address after setting: {global_vars.esp_car_ip_address}")

print("Connection completed")

#('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
