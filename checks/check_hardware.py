import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


# Green LED
greenLED = 18
# Red LED
redLED = 23
# Servo X
servoX = 18
# Servo Y
servoY = 23
# Relay Pin
relay = 12

GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(servoX, GPIO.OUT)
GPIO.setup(servoY, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)

class Test:
    pwmX = GPIO.PWM(servoX, 50)
    pwmY = GPIO.PWM(servoY, 50)

    pwmX.start(0)
    pwmY.start(0)

    def test_arm(self):
        # Arm the turret
        print("Arming Turret...")
        GPIO.output(greenLED, GPIO.LOW)
        GPIO.output(redLED, GPIO.HIGH)
        print("Turret Armed")
        
    def test_disarm(self):
        # Disarm the turret
        print("Disarming Turret...")
        GPIO.output(greenLED, GPIO.HIGH)
        GPIO.output(redLED, GPIO.LOW)
        print("Turret Disarmed")

    def test_fire():
        GPIO.output(relay, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(relay, GPIO.LOW)

    def to_duty_cycle(angle):
        return (angle/18) + 2.5

    def test_servos():
        for i in range(0,180,10):
            duty = Test.to_duty_cycle(i)
            Test.pwmX.ChangeDutyCycle(duty)
            Test.pwmY.ChangeDutyCycle(duty)
            time.sleep(0.5)
        for i in range(180,0,-10):
            duty = Test.to_duty_cycle(i)
            Test.pwmX.ChangeDutyCycle(duty)
            Test.pwmY.ChangeDutyCycle(duty)
            time.sleep(0.5)
    

while True:
    Test.test_arm()
    Test.test_servos()
    Test.test_fire()
    Test.test_disarm()