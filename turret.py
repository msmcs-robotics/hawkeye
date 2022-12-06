import RPi.GPIO as GPIO
from colorama import Fore
from playsound import playsound
import time
import os
import serial

from smbus import SMBus

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Green LED
greenLED = 18
# Red LED
redLED = 23
# Servo X
servoX = 24
# Servo Y
servoY = 25
# Relay
relay = 12

# Set up the GPIO channels
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(servoX, GPIO.OUT)
GPIO.setup(servoY, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)

# Start PWM running on both servos, value of 0 (pulse off)
pwmX = GPIO.PWM(servoX, 50)
pwmY = GPIO.PWM(servoY, 50)
pwmX.start(0)
pwmY.start(0)


class Arduino_Turret:    
    # Really just forwards coordinates
    servo_max_degrees = 180

    # serial
    baud = 9600
    ard_tty = '/dev/ttyACM0'

    # i2c
    ard1_addr = 0x08

    def fire(self, x, y):
        # send the coordinates to the arduino over serial
        # format: (x, y)

        with serial.Serial(self.ard_tty, self.baud, timeout=1) as arduino:
            if arduino.isOpen():
                arduino.write(bytes(f'{x},{y}', 'utf-8'))
                print(f'{Fore.GREEN}Firing at {x}, {y}{Fore.RESET}')

    
class Pi_Turret:
    
    # Turret System attached to the Raspberry Pi

    # Don't attach camera to moving parts of the turret so the frames don't drastically change
    def arm(self):
        # Arm the turret
        print("Arming Turret...")
        GPIO.output(greenLED, GPIO.LOW)
        GPIO.output(redLED, GPIO.HIGH)
        print("Turret Armed")
    
    def disarm(self):
        # Disarm the turret
        print("Disarming Turret...")
        GPIO.output(greenLED, GPIO.HIGH)
        GPIO.output(redLED, GPIO.LOW)
        print("Turret Disarmed")

    def aim(duty_cycle_x, duty_cycle_y):
        pwmX.ChangeDutyCycle(duty_cycle_x)
        pwmY.ChangeDutyCycle(duty_cycle_y)

    def fire(x, y):
        Pi_Turret.arm()
        Pi_Turret.aim(x, y)
        #print(Fore.BLUE + "Firing...")
        #print(Fore.YELLOW + "Firing at coordinates: {}, {}".format(self.x, self.y))
        GPIO.output(relay, GPIO.HIGH)
        time.sleep(2) # 2 second bursts
        GPIO.output(relay, GPIO.LOW)
        Pi_Turret.disarm()

class Alarm:
    
    # Alarm System

    def sound_alarm():
        print(Fore.BLUE + "Alarm is sounding...")
        playsound("assets/alarm.mp3", False)