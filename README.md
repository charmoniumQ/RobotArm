Robot Arm by Sam G
==================

***

###### Please read me ######

This is code for controlling servos through an arduino through a computer.
This is a hobbyist program for Science Olympiad's Robot Arm event.
Below, I have explained the contents of this project.
Feel free to fork! Submit a pull request and I will try to get back to you as soon as possible.


***

###### `arduino-side` has all the code for the arduino ######

1. `StandardFirmata.ino`:  Arduino's default Firmata implementation
  - TODO: mod the Firmata implementation for Stepper Motors

***

###### `computer-side` has all the code for the computer ######

1. `master.py`
  - This contains GUI code
  - This is the runable file
  - This file spawns all of the subprocesses
  - All pyGame events are processed here
  - Delegates events and other tasks to `automatic_control.py` and `manual_control.py`
2. `automatic_control.py`
  - This contains code that controls the Robot autonomously
  - Although the specific routine is autonomous, you can still spontaneously start/stop/skip to next/go to last...
  - Sends commands to `servo.py`
3. `manual_control.py`
  - This contains code that controls the Robot with a joystick
  - It supports several different modes
  - Sends commands to `servo.py`
4. `servo.py`
  - This contains code for manipulating servos
  - Can manipulate servos individually, or can manipulate the robot as a whole
  - It sends commands to `communication.py`
5. `communication.py`
  - This code contains the specifics about communicating with arduinos
  - Uses pyFirmata to communicate over a serial port with the arduino
  - It sends firmata data over serial to the arduino
