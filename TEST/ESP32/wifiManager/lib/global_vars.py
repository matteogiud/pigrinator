esp_car_ip_address = None

def set_esp_car_ip_address(ip_address):
    global  esp_car_ip_address
    esp_car_ip_address = ip_address
    
def get_esp_car_ip_address():
    global  esp_car_ip_address
    return esp_car_ip_address
    