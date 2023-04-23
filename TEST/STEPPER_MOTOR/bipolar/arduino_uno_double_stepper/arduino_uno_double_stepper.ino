// Include the Arduino Stepper Library

#include <Stepper.h>

// Number of steps per output rotation
const int stepsPerRevolution = 32;

// Create Instance of Stepper library
Stepper myStepperA(stepsPerRevolution, 13, 12, 14, 27);
Stepper myStepperB(stepsPerRevolution, 26, 25, 33, 32);


void setup() {
  // set the speed at 60 rpm:
  myStepperA.setSpeed(1000); //fast at 1500
  myStepperB.setSpeed(1000);
  // initialize the serial port:
  Serial.begin(115200);
}

void loop() {
  // step one revolution in one direction:
  Serial.println("clockwise");
  for (int i = 0; i < 2048; i++) {
    myStepperA.step(1);
    myStepperB.step(1);
  }
  delay(500);

}