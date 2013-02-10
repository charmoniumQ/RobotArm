#include <Stepper.h>
#include "Stepper.h"

Stepper steppers[MAX_STEPPERS];

void doStepperCommand(byte pin, byte byteCount, byte *arrayPointer) {
  if (arrayPointer[0] != STEPPER_COMMAND)
    return;
  switch (arrayPointer[1]) {
    case STEPPER_SETUP_S:
      if (byteCount != 6)
        return;
      stepper[arrayPointer[2]] = Stepper(arrayPointer[3], arrayPointer[4], arrayPointer[5]);
      break;
    case STEPPER_SETUP_C:
      if (byteCount != 8)
        return;
      stepper[arrayPointer[2]] = Stepper(arrayPointer[3], arrayPointer[4], arrayPointer[5], arrayPointer[6], arrayPointer[7]);
      break;
    case STEPPER_SPEED:
      if (byteCount != 4)
        return;
      stepper[arrayPointer[2]].setSpeed(arrayPointer[3]);
      break;
    case STEPPER_STEPS:
      if (byteCount != 4)
        return;
      stepper[arrayPointer[2]].step(arrayPointer[3]);
      break;
    default:
      break;
  }
}
