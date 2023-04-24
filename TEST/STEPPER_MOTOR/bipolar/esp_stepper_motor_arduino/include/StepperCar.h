#include <Stepper.h>
#include <Arduino.h>
#ifndef StepperCar_h
#define StepperCar_h_h

class StepperCar
{
public:
  StepperCar(Stepper &motor_1, Stepper &motor_2) : motor_1(motor_1),
                                                   motor_2(motor_2)
  {
    this->wheels_circumference_cm = 6.7 * 3.1416;
    this->steps_per_round_complete = 2038;
    this->wheels_distances_circumference_cm = 13.5 * 3.1416;
  }
  void forward_cm(int distance_cm);
  void backward_cm(int distance_cm);
  void left(int degrees);
  void right(int degrees);

private:
  float wheels_circumference_cm, wheels_distances_circumference_cm;
  Stepper &motor_1, &motor_2;
  int steps_per_round_complete;
};

#endif