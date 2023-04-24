
#include "StepperCar.h"

const int steps_per_revolution = 32;

Stepper stp1(steps_per_revolution, 13, 12, 14, 27);
Stepper stp2(steps_per_revolution, 26, 25, 33, 32);
StepperCar stp_car(stp1, stp2);
void setup()
{
  Serial.begin(115200);
  stp1.setSpeed(1000);
  stp2.setSpeed(1000);
}

void loop()
{
  stp_car.forward_cm(20);
  delay(1000);

  stp_car.left(90);
  delay(1000);
}