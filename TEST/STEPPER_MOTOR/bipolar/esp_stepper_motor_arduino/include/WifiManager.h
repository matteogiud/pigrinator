#include <WiFi.h>
#include <esp_now.h>
#include <Arduino.h>
#ifdef WifiManager_h
#define WifiManager_h


class WifiManager{
    private:


    public:
        boolean isConnectedToWifi();
        ip4_addr1 ip;

};

#endif