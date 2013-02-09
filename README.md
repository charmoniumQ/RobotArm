Robot Arm by Sam G
==================

***

###### Please read me ######

This is code for controlling servos through an arduino through a computer.
This is a hobbyist program for Science Olympiad's Robot Arm event.
Below, I have explained the contents of this project.
Feel free to fork! Submit a pull request and I will try to get back to you as soon as possible.

***

###### Instalation ######
1. Upload `StandardFirmata.ino` to your arduino
2. Connect Servos to power source (I recomend to use an offboard power source)
3. Connect the Servos signal pin to the board
4. Goto `joystick.py` and update lines 26-32 (the definition of `self.bot`).
  - The first argument is the digital pin number that you are connected the servo to
  - The second argument is minpulse
  - The third argument is maxpulse
  - The fourth argument is starting angle
  - the last argument is length
    (this is obsolete and not ever used in this project).
    It was useful for deducing angles from an input of cartesian XYZ coordinates,
    But this feature never got implemented.
5. Install pySerial and pyFirmata (in that order)
6. Connect a ps-2/3 controller and an arduino uno
7. Run `joystick.py` and have fun!
