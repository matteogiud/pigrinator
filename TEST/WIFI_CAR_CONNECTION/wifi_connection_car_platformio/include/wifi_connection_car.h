#ifndef WIFI_CONNECTION_CAR_H
#define WIFI_CONNECTION_CAR_H

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char *ssid = "PIGRINATOR";
const char *password = "";
const char *serverGetPswCredential = "http://192.168.4.1/getWifiCredential"; // sostituisci con l'URL del server a cui vuoi fare la richiesta GET
const char *serverShutdown = "http://192.168.4.1/shutdown";                  // sostituisci con l'URL del server a cui vuoi fare la richiesta GET
const int esp_led = 2;
const char jsonPayload[] = "{\"mac_address\":\"C8:F0:9E:53:14:EC\"}";

void connect_to_wifi()
{

    pinMode(esp_led, OUTPUT);

    Serial.println();
    Serial.print("[WiFi_station] Connecting to esp station...");
    Serial.println(ssid);

    bool notConnected = true;
    while (notConnected) // finchè non è connesso allo stand prova a connettersi
    {
        WiFi.begin(ssid, password); // connessione alla rete
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
    }
    // prova a richiedere la psw del wifi allo stand
    

    HTTPClient http;                    // crea una richiesta http
    http.begin(serverGetPswCredential); // inizializza la richiesta

    http.addHeader("Content-Type", "application/json"); // aggiunge un header alla richiesta

    bool haveCredential = false;
    while (!haveCredential) // finchè non ha le credenziali richieste continua a richiederle
    {
        int httpResponseCode = http.POST(jsonPayload); // fa la richiesta
        Serial.println("[WiFi_request] Request Credential");
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
                String ssid = doc["ssid"]; // leggo il ssid
                String psw = doc["psw"]; // leggo la password
                Serial.print("[WiFi_request] SSID: ");
                Serial.print(ssid);
                Serial.print("\t[WiFi_request] PASSWORD: ");
                Serial.println(psw);

                http.end(); //chiudo la richiesta

                http.begin(serverShutdown); //inizializzo una nuova richiesta per lo spegnimento dell'ap
                http.addHeader("Content-Type", "application/json"); //aggiungo un header alla richiesta

                http.POST(jsonPayload); // chiudo l'ap mandandogli come payload il mio indirizzo MAC

                WiFi.disconnect(); // mi disconnetto dall'esp
                delay(1000);
                WiFi.begin(ssid.c_str(), psw.c_str());
                delay(2000);
                if (WiFi.status() == WL_CONNECTED)
                {
                    Serial.println("connected");
                    digitalWrite(esp_led, HIGH);
                    notConnected = false;
                }
                else
                {
                    Serial.print("not connected\r\nrestarting...");
                    delay(500);
                    ESP.restart();
                }
            }
        }
        else
        {
            notConnected = true;
        }
    }
}

#endif
