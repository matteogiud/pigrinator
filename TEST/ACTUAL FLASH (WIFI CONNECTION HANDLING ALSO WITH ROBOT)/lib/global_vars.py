my_vars = {"esp_car_ip_address": None}
esp_car_ip_address: str = None

def init():
    global my_vars
    global esp_car_ip_address
    my_vars = {"esp_car_ip_address": None}
    esp_car_ip_address = None
    