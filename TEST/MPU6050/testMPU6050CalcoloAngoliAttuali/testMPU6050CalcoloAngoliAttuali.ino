#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);
void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}

unsigned long t1, dt;
float x, y, z;
void loop() {
  mpu6050.update();
  dt = millis() - t1;
  if (dt >= 200) {
    x = mpu6050.getAngleX();
    y = mpu6050.getAngleY();
    z = mpu6050.getAngleZ();

    Serial.println("=======================================================");
   /* Serial.print("temp : ");
    Serial.println(mpu6050.getTemp());
    Serial.print("accX : ");
    Serial.print(mpu6050.getAccX());
    Serial.print("\taccY : ");
    Serial.print(mpu6050.getAccY());
    Serial.print("\taccZ : ");
    Serial.println(mpu6050.getAccZ());

    Serial.print("gyroX : ");
    Serial.print(mpu6050.getGyroX());
    Serial.print("\tgyroY : ");
    Serial.print(mpu6050.getGyroY());
    Serial.print("\tgyroZ : ");
    Serial.println(mpu6050.getGyroZ());

    Serial.print("accAngleX : ");
    Serial.print(mpu6050.getAccAngleX());
    Serial.print("\taccAngleY : ");
    Serial.println(mpu6050.getAccAngleY());

    Serial.print("gyroAngleX : ");
    Serial.print(mpu6050.getGyroAngleX());
    Serial.print("\tgyroAngleY : ");
    Serial.print(mpu6050.getGyroAngleY());
    Serial.print("\tgyroAngleZ : ");
    Serial.println(mpu6050.getGyroAngleZ());*/

    Serial.print("angleX : ");
    Serial.print(mpu6050.getAngleX());
    Serial.print("\tangleY : ");
    Serial.print(mpu6050.getAngleY());
    Serial.print("\tangleZ : ");
    Serial.println(mpu6050.getAngleZ());
    Serial.println("=======================================================\n");
  }
}