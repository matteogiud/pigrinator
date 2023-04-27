esp_car_ip_address: str = None
esp_car_mdns_hostname: str = None

def init():
    global esp_car_ip_address
    global esp_car_mdns_hostname
    
    esp_car_ip_address = None
    esp_car_mdns_hostname = None