#include <Wire.h>
#include <WiFi.h>
#include <WebServer.h>
#include <SparkFun_MPU6050.h>
#include <SparkFun_TB6612.h>

// Impostazioni WiFi
const char* ssid = "nomedellawifinetwork";
const char* password = "passworddellawifinetwork";

// Impostazioni del server web
WebServer server(80);

// Impostazioni del sensore MPU6050
MPU6050 mpu;

// Impostazioni dei motori
#define MOTOR_A_IN1 12
#define MOTOR_A_IN2 14
#define MOTOR_A_PWM 27
#define MOTOR_B_IN1 26
#define MOTOR_B_IN2 25
#define MOTOR_B_PWM 33
#define MOTOR_C_IN1 32
#define MOTOR_C_IN2 15
#define MOTOR_C_PWM 13
#define MOTOR_D_IN1 23
#define MOTOR_D_IN2 22
#define MOTOR_D_PWM 21
TB6612 motorA(MOTOR_A_IN1, MOTOR_A_IN2, MOTOR_A_PWM, 100);
TB6612 motorB(MOTOR_B_IN1, MOTOR_B_IN2, MOTOR_B_PWM, 100);
TB6612 motorC(MOTOR_C_IN1, MOTOR_C_IN2, MOTOR_C_PWM, 100);
TB6612 motorD(MOTOR_D_IN1, MOTOR_D_IN2, MOTOR_D_PWM, 100);

// Impostazioni del percorso
const int numPoints = 4;
const float path[numPoints][2] = { { 0.0, 0.0 }, { 1.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 1.0 } };

// Impostazioni del movimento
const float maxSpeed = 0.5;       // in metri al secondo
const float wheelDiameter = 0.1;  // in metri
const float wheelBase = 0.2;      // in metri

// Variabili globali del movimento
float currentX = 0.0;
float currentY = 0.0;
float currentHeading = 0.0;

// Funzione per muovere il robot da un punto all'altro
void move(float x, float y) {
  // Calcola la distanza da percorrere e la direzione del movimento
  float dx = x - currentX;
  float dy = y - currentY;
  float distance = sqrt(dx * dx + dy * dy);
  float heading = atan2(dy, dx) - currentHeading;

  // Imposta la velocità dei motori in base alla distanza da percorrere
  float speed = maxSpeed;
  if (distance < wheelBase / 2.0) {
    speed *= distance / (wheelBase / 2.0);
  }

  // Ruota il robot nella direzione corretta
  motorA.drive(0, speed * sin(heading));
  motorB.drive(0, speed * sin(heading));
  motorC.drive(0, speed * cos(heading));
  motorD.drive(0, speed * cos(heading));

  // Muove il robot per la durata del movimento
  float duration = distance / speed;
  delay(duration * 1000);

  // Aggiorna la posizione corrente del robot
  currentX = x;
  currentY = y;
  currentHeading = atan2(sin(currentHeading + heading), cos(currentHeading + heading));

  // Arresta i motori
  motorA.brake();
  motorB.brake();
  motorC.brake();
  motorD.brake();
}

// Funzione per tornare al punto di partenza
void returnHome() {
  // Muove il robot lungo il percorso in senso inverso
  for (int i = numPoints - 1; i >= 0; i--) {
    move(path[i][0], path[i][1]);
  }

  // Arresta i motori e resetta la posizione corrente del robot
  motorA.brake();
  motorB.brake();
  motorC.brake();
  motorD.brake();
  currentX = 0.0;
  currentY = 0.0;
  currentHeading = 0.0;
}

void setup() {
  // Inizializza il sensore MPU6050
  Wire.begin();
  mpu.begin();

  // Inizializza i motori
  motorA.begin();
  motorB.begin();
  motorC.begin();
  motorD.begin();

  // Connette il dispositivo alla rete WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  // Avvia il server web e mostra l'indirizzo IP del dispositivo
  server.on("/", {
    server.send(200, "text/plain", WiFi.localIP().toString());
  });
  server.begin();
}

void loop() {
  // Gestisce le richieste HTTP
  server.handleClient();

  // Legge i dati dal sensore MPU6050
  Vector3 accel = mpu.readRawAccel();
  Vector3 gyro = mpu.readRawGyro();

  // Calcola l'angolo di inclinazione del dispositivo
  float accelX = accel.x * 9.81 / 16384.0;
  float accelY = accel.y * 9.81 / 16384.0;
  float accelZ = accel.z * 9.81 / 16384.0;
  float pitch = atan2(-accelX, sqrt(accelYaccelY + accelZaccelZ));
  float roll = atan2(accelY, accelZ);

  // Calcola la velocità di rotazione del dispositivo
  float gyroX = gyro.x * 500.0 / 32768.0;
  float gyroY = gyro.y * 500.0 / 32768.0;
  float gyroZ = gyro.z * 500.0 / 32768.0;
  float rotationRate = sqrt(gyroXgyroX + gyroYgyroY + gyroZ * gyroZ);

  // Se la velocità di rotazione è inferiore a una soglia, il dispositivo si muove
  if (rotationRate < 0.1) {
    // Calcola la posizione del dispositivo
    float cosPitch = cos(pitch);
    float sinPitch = sin(pitch);
    float cosRoll = cos(roll);
    float sinRoll = sin(roll);
    float x = cosRoll * cosPitch;
    float y = sinRoll * cosPitch;
    float heading = atan2(y, x);

    // Aggiorna la posizione corrente del robot
    currentX += cos(heading) * wheelDiameter / 2.0;
    currentY += sin(heading) * wheelDiameter / 2.0;
    // Aggiorna la direzione corrente del robot
    currentHeading = heading;

    // Controlla se il robot ha raggiunto il punto di destinazione
    if (currentX == targetX && currentY == targetY) {
      // Se il robot ha raggiunto il punto di destinazione, calcola il nuovo punto di destinazione
      if (currentPoint < numPoints) {
        targetX = path[currentPoint][0];
        targetY = path[currentPoint][1];
        currentPoint++;
      }
      // Se il robot ha raggiunto il punto finale, torna al punto di partenza
      else {
        returnHome();
      }
    }
    // Altrimenti, muovi il robot verso il punto di destinazione
    else {
      move(targetX, targetY);
    }
  }
}