#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
const char* ssid = "PIGRINATOR";
const char* password = "";
const char* serverGetPswCredential = "http://192.168.4.1/getWifiCredential";  // sostituisci con l'URL del server a cui vuoi fare la richiesta GET
const char* serverShutdown = "http://192.168.4.1/shutdown";                   // sostituisci con l'URL del server a cui vuoi fare la richiesta GET
const int esp_led = 2;
const char jsonPayload[] = "{\"mac_address\":\"C8:F0:9E:53:14:EC\"}";




void connect_to_wifi() {
  Serial.begin(115200);

  Serial.println();
  Serial.print("[WiFi] Connecting to ");
  Serial.println(ssid);
  pinMode(esp_led, OUTPUT);


  bool notConnected = true;
  while (notConnected) {
    WiFi.begin(ssid, password);
    delay(3000);
    switch (WiFi.status()) {
      case WL_CONNECTED:
        Serial.println("connected");
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());
        notConnected = false;
        break;
      default:
        Serial.println("retry to connect");
    }
  }
  Serial.println("start request");
  HTTPClient http;
  http.begin(serverGetPswCredential);


  http.addHeader("Content-Type", "application/json");

  notConnected = true;
  while (notConnected) {
    int httpResponseCode = http.POST(jsonPayload);
    if (httpResponseCode == 200) {
      Serial.println("devo connettermi");
      // Leggere la risposta del server
      String credentials = http.getString();
      DynamicJsonDocument doc(1024);

      DeserializationError error = deserializeJson(doc, credentials);

      if (error) {
        Serial.print(F("Errore durante la deserializzazione: "));
        Serial.println(error.c_str());
        notConnected = true;
      } else {
        String ssid = doc["ssid"];
        String psw = doc["psw"];
        Serial.print("ssid: ");
        Serial.println(ssid);
        Serial.print("password: ");
        Serial.println(psw);

        http.end();

        http.begin(serverShutdown);
        http.addHeader("Content-Type", "application/json");
        //int retryTime = 10;
        http.POST(jsonPayload);//close ap

        WiFi.disconnect();
        delay(1000);
        WiFi.begin(ssid.c_str(), psw.c_str());
        delay(2000);
        if (WiFi.status() == WL_CONNECTED) {
          Serial.println("connected");
          digitalWrite(esp_led, HIGH);
          notConnected = false;




        } else {
          Serial.print("not connected\r\nrestarting...");
          delay(500);
          ESP.restart();
        }
      }


    } else {
      notConnected = true;
    }
  }
}
