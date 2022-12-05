from turret import Arduino_Turret
from time import sleep

for i in range(0, Arduino_Turret.servo_max_degrees, 10):
    Arduino_Turret.fire(i, i)
    sleep(0.1)

for i in range(Arduino_Turret.servo_max_degrees, 0, -10):
    Arduino_Turret.fire(i, i)
    sleep(0.1)