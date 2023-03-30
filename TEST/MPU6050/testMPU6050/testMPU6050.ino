#include <Wire.h>
#include <MPU6050_tockn.h>

// Impostazioni del sensore MPU6050
MPU6050 mpu(Wire);


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


void setup() {
  // Inizializza il sensore MPU6050
  Serial.begin(115200);
  Wire.begin();
  mpu.begin();
  mpu.calcGyroOffsets(true);
}

void loop() {
  mpu.update();
  // Legge i dati dal sensore MPU6050
  float accel[3] = { mpu.getAccX(), mpu.getAccY(), mpu.getAccY() };
  float gyro[3] = { mpu.getGyroX(), mpu.getGyroY(), mpu.getGyroZ() };

  // Calcola l'angolo di inclinazione del dispositivo
  float accelX = accel[0] * 9.81 / 16384.0;
  float accelY = accel[1] * 9.81 / 16384.0;
  float accelZ = accel[2] * 9.81 / 16384.0;
  float pitch = atan2(-accelX, sqrt(accelY + accelZ));
  float roll = atan2(accelY, accelZ);

  /*Serial.print("Angolo inclinazione: ");
  Serial.println(roll);*/

  // Calcola la velocità di rotazione del dispositivo
  double gyroX = gyro[0] * 500.0 / 32768.0;
  double gyroY = gyro[1] * 500.0 / 32768.0;
  double gyroZ = gyro[2] * 500.0 / 32768.0;
  double rotationRate = sqrt(gyroX * gyroX + gyroY * gyroY + gyroZ * gyroZ);

  /*Serial.print("Velocità rotazione: ");
  Serial.println(rotationRate);*/

  // Se la velocità di rotazione è inferiore a una soglia, il dispositivo si muove
  if (rotationRate < 0.1) {
    // Calcola la posizione del dispositivo
    float cosPitch = cos(pitch);
    [[maybe_unused]] float sinPitch = sin(pitch);
    float cosRoll = cos(roll);
    float sinRoll = sin(roll);
    float x = cosRoll * cosPitch;
    float y = sinRoll * cosPitch;
    float heading = atan2(y, x);
    Serial.print("AccelX: ");
    Serial.print(sqrt(accelY * accelY + accelZ * accelZ));
    Serial.print(" AccelY: ");
    Serial.print(accelY);
    Serial.print(" AccelZ: ");
    Serial.println(accelZ);
    // Aggiorna la posizione corrente del robot
    currentX += cos(heading) * wheelDiameter / 2.0;
    currentY += sin(heading) * wheelDiameter / 2.0;
    // Aggiorna la direzione corrente del robot
    currentHeading = heading;
    /*Serial.print("Posizione Corrente: X: ");
    Serial.print(currentX);
    Serial.print(" Y: ");
    Serial.println(currentY);*/
  }
}