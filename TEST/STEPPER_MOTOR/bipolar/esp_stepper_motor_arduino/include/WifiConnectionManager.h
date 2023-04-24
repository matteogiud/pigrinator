#include <esp_now.h>
#include <WiFi.h>

#ifdef WifiConnectionManager_h
#define WifiConnectionManager_h

class WifiConnectionManager
{

    private:
    
public:
    WifiConnectionManager(){};
    boolean isConnectedToWifi();
    ip4_addr1 ip;

    // Structure example to send data
    // Must match the receiver structure
    typedef struct struct_message
    {
        /*records*/
    } struct_message;

    esp_now_peer_info_t peerInfo;

    void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status);
    void OnDataRecv(const uint8_t *mac, const uint8_t *incomingData, int len);
    void initConnection();
};

#endif