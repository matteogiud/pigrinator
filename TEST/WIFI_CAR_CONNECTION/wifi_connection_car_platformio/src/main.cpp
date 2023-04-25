#include <Arduino.h>
#include "wifi_connection_car.h"
#include <WebServer.h>
#include <ArduinoJson.h>

const char *esp_ssid = "PIGRINATOR";
const char *esp_psw = "";
const char *my_esp_station_ip;
WebServer server(80);
bool buisy = false;

StaticJsonDocument<250> jsonDocument;
char buffer[250];

void go_to_destination()
{
  buisy = true;

  int numPairs = jsonDocument.size();

  for (const auto &kv : jsonDocument.as<JsonObject>())
  {
    const String &key = kv.key().c_str();
    const int value = kv.value().as<int>();

    delay(1000);

    if (key == "forward")
    {
      /* car.forward(value); */
    }
    else if (key == "backward")
    {
      /* car.backward(value); */
    }
    else if (key == "left")
    {
      /* car.left(value); */
    }
    else if (key == "right")
    {
      /* car.right(value); */
    }

    // Stampa la chiave e il valore
    Serial.print("Chiave: ");
    Serial.print(key);
    Serial.print(", Valore: ");
    Serial.println(value);
  }
  buisy = false;
}

void return_to_station()
{
  buisy = true;
  int numPairs = jsonDocument.size();

  for (auto it = jsonDocument.as<JsonObject>().begin(); it != jsonDocument.as<JsonObject>().end(); ++it)
  {
    const String &key = it->key().c_str();
    const int value = it->value().as<int>();

    delay(1000);

    if (key == "forward")
    {
      /* car.backward(value); */
    }
    else if (key == "backward")
    {
      /* car.forward(value); */
    }
    else if (key == "left")
    {
      /* car.right(value); */
    }
    else if (key == "right")
    {
      /* car.left(value); */
    }

    // Stampa la chiave e il valore
    Serial.print("Chiave: ");
    Serial.print(key);
    Serial.print(", Valore: ");
    Serial.println(value);
  }
  buisy = false;
}

void followThisPathHandler()
{
  Serial.println("[\\followThisPath] new request");
  if (buisy)
  {
    server.send(500, "text/plain", "Buisy");
    return;
  }
  // put your main code here, to run repeatedly:
  String body = server.arg("plain");
  DeserializationError error = deserializeJson(jsonDocument, body);

  if (error)
  {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    server.send(500, "text/plain", "deserializeJson() failed");
    buisy = false;
    return;
  }

  server.send(200, "text/plain", "ok");
  buisy = true;
  go_to_destination();
  Serial.println("arrived to destination");
  delay(20000);
  return_to_station();
  Serial.println("returned to station");
  buisy = false;
}

void indexHandler()
{
  Serial.println("[\\] new request");

  server.send(200, "text/plain", "hello");
}
void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  my_esp_station_ip = connect_to_wifi(esp_ssid, esp_psw);
  if (my_esp_station_ip == nullptr)
  { // se non si collega
    Serial.println("Connessione fallita");
  }
  else
  {
    Serial.println("Connessione avvenuta");
  }

  server.on("/followThisPath", HTTP_POST, followThisPathHandler);
  server.on("/", indexHandler);
  server.begin();
}

void loop()
{
  server.handleClient();
}