#include <Stepper.h>
#ifndef stepper_car_h
#define stepper_car_h


class StepperCar{
  public:
    StepperCar(Stepper motor_1, Stepper motor_2);
    void forward_cm(int distance_cm);
    void backward_cm(int distance_cm);
    void left(int degrees);
    void right(int degrees);

  private:
    float wheels_circumference_cm, wheels_distances_circumference_cm; 
    Stepper motor_1, motor_2;
    int steps_per_round_complete;

};

#endif