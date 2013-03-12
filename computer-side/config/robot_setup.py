servos = [
    ('waist', 7, (900, 1100), 90, (0, 30)),
    ('shoulder', 6, (600, 2400), 60, (30, 150)),
    ('elbow', 5, (600, 2400), 50, (0, 180), .1),
    ('wrist', 4, (600, 2400)),
    ('claw', 3, (600, 2400)),
]
port_name = 'F'
#port_name = 'R:/dev/ttyUSB*'
baud_rate = 57600
object_name = 'Robot over Serial'
