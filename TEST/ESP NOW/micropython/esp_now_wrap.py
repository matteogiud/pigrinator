import network
import espnow

class espNowWrapper:
    def __init__(self, peer_mac_addr: bytes, recv_function, active=True):
        sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
        sta.active(True)
        self.e = espnow.ESPNow();
        e.active(True)
        self.peer_mac_addr = peer_mac_addr
        self.e.add_peer(peer)
        self.e.irq(recv_function, self.e)
        
    def send_message(message: str):
        self.e.send(message)

        
        
        