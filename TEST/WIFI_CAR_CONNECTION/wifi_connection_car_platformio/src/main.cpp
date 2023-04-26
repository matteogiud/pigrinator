#include <Arduino.h>
#include "wifi_connection_car.h"
#include <WebServer.h>
#include <ArduinoJson.h>
#include "StepperCar.h"
#include <map>

const char *esp_ssid = "PIGRINATOR";
const char *esp_psw = "";
const char *my_esp_station_ip;
const int steps_per_revolution = 32;

WebServer server(80);
bool buisy = false;

Stepper stp1(steps_per_revolution, 13, 12, 14, 27);
Stepper stp2(steps_per_revolution, 26, 25, 33, 32);
StepperCar stp_car(stp1, stp2);

StaticJsonDocument<250> jsonDocument;
std::map<String, int> jsonOrderedMap;


void blinkBlueLed()
{
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
}


void go_to_destination()
{
  //buisy = true;

  for (size_t i = 0; i < jsonDocument.size(); i++)
  {
    const char *direction = jsonDocument[i]["direction"];
    int value = jsonDocument[i]["value"];
    
    // Esegui il metodo corrispondente in base alla direzione
    if (strcmp(direction, "right") == 0)
    {
      Serial.println("right: " + String(value));
      stp_car.right(value);
    }
    else if (strcmp(direction, "left") == 0)
    {
      Serial.println("left: " + String(value));
      stp_car.left(value);
    }
    else if (strcmp(direction, "forward") == 0)
    {
      Serial.println("forward: " + String(value));
      stp_car.forward_cm(value);
    }
    else if (strcmp(direction, "backward") == 0)
    {
      Serial.println("backward: " + String(value));
      stp_car.backward_cm(value);
    }
    else
    {
      // Direzione non riconosciuta, stampa un messaggio di errore
      Serial.println("Direzione non riconosciuta");
      //buisy = false;
      throw std::runtime_error("Direzione non riconosciuta");
    }
    delay(1500);
  }
  // int numPairs = jsonDocument.size();
  // for (const auto &kv : jsonDocument.as<JsonObject>())
  // {
  //   const String &key = kv.key().c_str();
  //   const int value = kv.value().as<int>();

  //   delay(1000);

  //   if (key == "forward")
  //   {
  //     /* car.forward(value); */
  //     stp_car.forward_cm(value);
  //   }
  //   else if (key == "backward")
  //   {
  //     /* car.backward(value); */
  //     stp_car.backward_cm(value);
  //   }
  //   else if (key == "left")
  //   {
  //     /* car.left(value); */
  //     stp_car.left(value);
  //   }
  //   else if (key == "right")
  //   {
  //     /* car.right(value); */
  //     stp_car.right(value);
  //   }

  // jsonOrderedMap.insert({key, value});

  // Stampa la chiave e il valore
  // Serial.print("Chiave: ");
  // Serial.print(key);
  // Serial.print(", Valore: ");
  // Serial.println(value);

  // buisy = false;
}

void return_to_station()
{
  //buisy = true;  

  for (size_t i = jsonDocument.size(); i > 0; i--)
  {
    delay(1500);
    const char *direction = jsonDocument[i-1]["direction"];
    int value = jsonDocument[i-1]["value"];
    // Esegui il metodo corrispondente in base alla direzione
    if (strcmp(direction, "right") == 0)
    {
      Serial.println("left: " + String(value));
      stp_car.left(value);
    }
    else if (strcmp(direction, "left") == 0)
    {
      Serial.println("right: " + String(value));
      stp_car.right(value);
    }
    else if (strcmp(direction, "forward") == 0)
    {
      Serial.println("backward: " + String(value));
      stp_car.backward_cm(value);
    }
    else if (strcmp(direction, "backward") == 0)
    {
      Serial.println("forward: " + String(value));
      stp_car.forward_cm(value);
    }
    else
    {
      // Direzione non riconosciuta, stampa un messaggio di errore
      Serial.println("Direzione non riconosciuta");
      //buisy = false;
      throw std::runtime_error("Direzione non riconosciuta");
    }
    
  }
  //buisy = false;
  // for (auto it = jsonOrderedMap.rbegin(); it != jsonOrderedMap.rend(); ++it)
  // {
  //   const String key = it->first;
  //   const int value = it->second;
  //   /*const String &key = it->key().c_str();
  //   const int value = it->value().as<int>();*/

  //   delay(1000);

  //   if (key == "forward")
  //   {
  //     /* car.backward(value); */
  //     stp_car.backward_cm(value);
  //   }
  //   else if (key == "backward")
  //   {
  //     /* car.forward(value); */
  //     stp_car.forward_cm(value);
  //   }
  //   else if (key == "left")
  //   {
  //     /* car.right(value); */
  //     stp_car.right(value);
  //   }
  //   else if (key == "right")
  //   {
  //     /* car.left(value); */
  //     stp_car.left(value);
  //   }

  //   // Stampa la chiave e il valore
  //   Serial.print("Chiave: ");
  //   Serial.print(key);
  //   Serial.print(", Valore: ");
  //   Serial.println(value);
  //}
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
  try
  {
    go_to_destination();
  }
  catch (const std::exception &e)
  {
    //buisy=false;
    Serial.println(e.what());
    return;
  }
  blinkBlueLed();
  Serial.println("arrived to destination");
  delay(5000);
  blinkBlueLed();
  delay(1000);
  try
  {
    return_to_station();
  }
  catch (const std::exception &e)
  {
    //buisy=false;
    Serial.println(e.what());
    return;
  }

  blinkBlueLed();
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

  pinMode(LED_BUILTIN, OUTPUT);

  stp1.setSpeed(1000);
  stp2.setSpeed(1000);

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
  server.on("/", indexHandler); // per controllare se funziona
  server.begin();
}

void loop()
{
  server.handleClient();
}