import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)

e = espnow.ESPNow()
e.active(True)
peer = b'\xc8\xf0\x9eS\x14\xec'   # MAC address of peer's wifi interface
e.add_peer(peer) # Must add_peer() before send()
while True:
    e.send(peer, "Starting...")
    for i in range(100):
        e.send(peer, str(i)*20, True)
    e.send(peer, b'end')

    

