#include <Arduino.h>
#define MAX_STEPPERS 10

#define STEPPER_COMMAND B01100000
#define STEPPER_SETUP_S B01100010
#define STEPPER_SETUP_C B01100001
#define STEPPER_SPEED   B01100011
#define STEPPER_STEPS   B01100100

void doStepperCommand(byte pin, byte byteCount, byte *arrayPointer)
