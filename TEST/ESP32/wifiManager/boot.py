from lib.wifi_manager import WIFIManager
from machine import Pin
from time import sleep

wifiManager = WIFIManager()

wifiManager.connect()