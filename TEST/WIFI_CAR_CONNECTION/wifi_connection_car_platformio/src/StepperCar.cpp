#include "StepperCar.h"

// StepperCar::StepperCar(Stepper &motor_1, Stepper &motor_2) : motor_1(motor_1),
//                                                              motor_2(motor_2)
// {
//   this->wheels_circumference_cm = 6.7 * 3.1416;
//   this->steps_per_round_complete = 2038;
//   this->wheels_distances_circumference_cm = 13.5 * 3.1416;
// }

void StepperCar::forward_cm(int distance_cm)
{
  int steps_to_do = abs((int)distance_cm * this->steps_per_round_complete / this->wheels_circumference_cm);

  for (int i = 0; i < steps_to_do; i++)
  {
    this->motor_1.step(-1);
    this->motor_2.step(-1);
  }
}

void StepperCar::backward_cm(int distance_cm)
{
  int steps_to_do = abs((int)distance_cm * this->steps_per_round_complete / this->wheels_circumference_cm);

  for (int i = 0; i < steps_to_do; i++)
  {
    this->motor_1.step(1);
    this->motor_2.step(1);
  }
}

void StepperCar::left(int degrees)
{
  int distance_cm = abs(this->wheels_distances_circumference_cm * degrees / 360);
  int steps_to_do = abs((int)distance_cm * this->steps_per_round_complete / this->wheels_circumference_cm);

  for (int i = 0; i < steps_to_do; i++)
  {
    this->motor_1.step(1);
    this->motor_2.step(-1);
  }
}

void StepperCar::right(int degrees)
{
  int distance_cm = abs(this->wheels_distances_circumference_cm * degrees / 360);
  int steps_to_do = abs((int)distance_cm * this->steps_per_round_complete / this->wheels_circumference_cm);

  for (int i = 0; i < steps_to_do; i++)
  {
    this->motor_1.step(-1);
    this->motor_2.step(1);
  }
}
