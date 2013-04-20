servos = [
    ('waist', 12, (900, 1100), 5090, (0, 30)),
    ('shoulder', 11, (600, 2400), 060, (0, 180)), # 30, 150
    ('elbow', 10, (600, 2400), 050, (50, 180), .1),
    ('wrist', 9, (600, 2400), 0),
    ('claw', 8, (600, 2400), 0),
]
#port_name = 'F'
port_name = 'R:/dev/ttyUSB*'
baud_rate = 57600
object_name = 'Robot over Serial'
