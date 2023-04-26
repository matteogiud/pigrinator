#ifndef WIFI_CONNECTION_CAR_H
#define WIFI_CONNECTION_CAR_H

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ESPmDNS.h>

// const char *esp_ssid = "PIGRINATOR";
// const char *esp_psw = "";

const char *hostname = "pigrinatorcar";
const char *serverGetPswCredential = "http://192.168.4.1/getWifiCredential"; // sostituisci con l'URL del server a cui vuoi fare la richiesta GET
const char *serverShutdown = "http://192.168.4.1/shutdown";                  // sostituisci con l'URL del server a cui vuoi fare la richiesta GET
const int esp_led = 2;
const char jsonPayload[] = "{\"mac_address\":\"C8:F0:9E:53:14:EC\"}";
String jsonPayloadShutdown = "{\"mac_address\":\"C8:F0:9E:53:14:EC\", \"actual_ip_address\":\"%%IPADDRESS%%\"}";
const char *esp_station_ip;

const char *connect_to_wifi(const char *esp_ssid, const char *esp_psw) // return esp_station_ip
{

    pinMode(esp_led, OUTPUT);

    Serial.println();
    Serial.print("[WiFi_station] Connecting to esp station...");
    Serial.println(esp_ssid);

    bool notConnected = true;
    int timeToTry = 20;
    while (notConnected) // finchè non è connesso allo stand prova a connettersi
    {
        WiFi.begin(esp_ssid, esp_psw); // connessione alla rete
        delay(3000);

        switch (WiFi.status()) // controllo lo stato della connessione
        {
        case WL_CONNECTED: // se la connessione è andata a buon fine
            Serial.println("[WiFi_station] Connected");
            Serial.print("[WiFi_station] IP Address: [");
            Serial.print(WiFi.localIP());
            Serial.println("]");

            notConnected = false; // dico che è connesso cosicchè esca dal ciclo
            break;
        default: // se non è connesso allo stand prova a riconnettersi
            Serial.println("[WiFi_station] Retrying to Connect");
        }
        timeToTry--;
        if (timeToTry < 0)
        {
            return nullptr;
        }
    }
    // prova a richiedere la psw del wifi allo stand

    HTTPClient http;                    // crea una richiesta http
    http.begin(serverGetPswCredential); // inizializza la richiesta

    http.addHeader("Content-Type", "application/json"); // aggiunge un header alla richiesta

    bool haveCredential = false;
    timeToTry = 20;
    while (!haveCredential) // finchè non ha le credenziali richieste continua a richiederle
    {
        int httpResponseCode = http.POST(jsonPayload); // fa la richiesta
        delay(2000);
        Serial.print("[WiFi_request] Request Credential: ");
        Serial.println(httpResponseCode);
        if (httpResponseCode == 200) // se la richiesta è andata a buon fine
        {
            Serial.println("[WiFi_request] Request Credential Success");
            // Leggere la risposta del server
            String credentials = http.getString();
            DynamicJsonDocument doc(1024);

            DeserializationError error = deserializeJson(doc, credentials);

            if (error) // se c'è un errore
            {
                Serial.print(F("[WiFi_request] Error During Deserialization: "));
                Serial.println(error.c_str());
                haveCredential = false; // dico che non ha le credenziali
            }
            else // se non ci sono errori nella deserializzazione
            {
                String wifi_ssid = doc["ssid"]; // leggo il ssid
                String wifi_psw = doc["psw"];   // leggo la password
                String sta_ip = doc["myIp"];    // leggo l'indirizzo IP
                esp_station_ip = sta_ip.c_str();
                Serial.print("[WiFi_request] SSID: ");
                Serial.print(wifi_ssid);
                Serial.print("\tPASSWORD: ");
                Serial.println(wifi_psw);
                Serial.print("\tHIS IP: ");
                Serial.println(esp_station_ip);

                http.end(); // chiudo la richiesta

                http.begin(serverShutdown);                         // inizializzo una nuova richiesta per lo spegnimento dell'ap
                http.addHeader("Content-Type", "application/json"); // aggiungo un header alla richiesta
                jsonPayloadShutdown.replace("%%IPADDRESS%%", hostname);
                http.POST(jsonPayloadShutdown); // chiudo l'ap mandandogli come payload il mio indirizzo MAC

                WiFi.disconnect(); // mi disconnetto dall'esp
                delay(1000);
                WiFi.begin(wifi_ssid.c_str(), wifi_psw.c_str()); // prova a connettersi al wifi che gli è stato fornito con la request
                delay(2000);
                if (WiFi.status() == WL_CONNECTED) // se la connessione è andata a buon fine
                {
                    if (MDNS.begin(hostname))
                    {
                        Serial.print("[WiFi_request] IP Address: [");
                        Serial.print(WiFi.localIP());
                        Serial.println("]");
                        Serial.println("[WiFi_request] Host Name: http://" + String(hostname) + ".local/");
                    }

                    Serial.print("[WiFi_request] Connected to ");
                    Serial.println(wifi_ssid);
                    digitalWrite(esp_led, HIGH);
                    haveCredential = true; // dico che ha le credenziali
                }
                else
                {
                    Serial.print("[WiFi_request] Not Nonnected"); // se non riesce a connettersi allora
                    delay(500);
                    return nullptr;
                }
            }
        }
        else
        {
            haveCredential = false; // se la richiesta non è andata a buon fine dico che non ha le credenziali
        }
        timeToTry--;
        if (timeToTry < 0)
        {
            return nullptr;
        }
    }
    return esp_station_ip;
}

#endif
