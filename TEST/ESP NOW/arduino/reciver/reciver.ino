#include <esp_now.h>
#include <WiFi.h>

char recive_message[32] = "";

void OnDataRecv(const uint8_t *mac, const uint8_t *imcomingData, int len){
  memcpy(&recive_message, imcomingData, sizeof(recive_message));
  Serial.print("len data received: ");
  Serial.println(len);
  Serial.print("Data: ");
  Serial.println(*imcomingData);
  Serial.println();
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);

  if(esp_now_init() != ESP_OK){
    Serial.println("error initializing esp-now");
    delay(25);
    ESP.restart();
  }

  esp_now_register_recv_cb(OnDataRecv);
  Serial.println("ready");
}

void loop() {
  // put your main code here, to run repeatedly:

}
