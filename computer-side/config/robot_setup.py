servos = [
	#name		pin	pulse_range,	start	angle_rnge	speed, sens, sens_exp
    ('waist',	12,	(900, 1100),	162,	(5,30),		1,		0.6,	2.5),
    ('shoulder',11,	(600, 2400),	43.52,	(75, 140),	1,		1.3,	2.0),
    ('elbow',	10,	(600, 2400),	20.125,	(20, 175),	1,		0.6,	1.5),
    ('wrist',	9,	(600, 2400),	97.55,	(2, 150),	1,		1.2,	1.2),
    ('claw',	8,	(600, 2400),	0,		(0, 180),	1,		2.5,	1.0),
]

port_name = 'F'
#port_name = 'R:/dev/tty.usb*'
#port_name = 'R:/dev/ttyUSB*'
baud_rate = 57600
object_name = 'Robot over Serial'
robot_sens = 1.2
robot_sens_exp = 1
