import esp_now_wrap
from time import sleep

esp_now = espNowWrapper(b'0xC80xF00x9E0x530x140xEC')

while True:

    esp_now.send_message("ciao esp")
    sleep(2)
