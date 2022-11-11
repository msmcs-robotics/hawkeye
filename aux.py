import RPi.GPIO as GPIO
import time
from playsound import playsound
from colorama import Fore

servoX = 17
servoY = 18

GPIO.setmode(GPIO.BCM)

using_steppers = False

if using_steppers:
    s1_i1 = 17
    s1_i2 = 17
    s1_i3 = 17
    s1_i4 = 17

    s2_i1 = 17
    s2_i2 = 17
    s2_i3 = 17
    s2_i4 = 17

    GPIO.setup(s1_i1, GPIO.OUT)
    GPIO.setup(s1_i2, GPIO.OUT)
    GPIO.setup(s1_i3, GPIO.OUT)
    GPIO.setup(s1_i4, GPIO.OUT)

    GPIO.output( s1_i1, GPIO.LOW )
    GPIO.output( s1_i2, GPIO.LOW )
    GPIO.output( s1_i3, GPIO.LOW )
    GPIO.output( s1_i4, GPIO.LOW )


    GPIO.setup(s2_i1, GPIO.OUT)
    GPIO.setup(s2_i2, GPIO.OUT)
    GPIO.setup(s2_i3, GPIO.OUT)
    GPIO.setup(s2_i4, GPIO.OUT)

    GPIO.output( s2_i1, GPIO.LOW )
    GPIO.output( s2_i2, GPIO.LOW )
    GPIO.output( s2_i3, GPIO.LOW )
    GPIO.output( s2_i4, GPIO.LOW )

    # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
    step_sleep = 0.002
    
    step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
    
    # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
    step_sequence = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]

    motor_pinsX = [s1_i1, s1_i2, s1_i3, s1_i4]
    motor_pinsY = [s2_i1, s2_i2, s2_i3, s2_i4]

elif not using_steppers:
    servoX = 17
    servoY = 18

    GPIO.setup(servoX, GPIO.OUT)
    GPIO.setup(servoY, GPIO.OUT)

    pX = GPIO.PWM(servoX, 50) # GPIO 17 for PWM with 50Hz
    pY = GPIO.PWM(servoY, 50) # GPIO 18 for PWM with 50Hz

    pX.start(0) # Initialization
    pY.start(0) # Initialization

class Turret:


    def cleanup():
        if using_steppers:
            GPIO.output( s1_i1, GPIO.LOW )
            GPIO.output( s1_i2, GPIO.LOW )
            GPIO.output( s1_i3, GPIO.LOW )
            GPIO.output( s1_i4, GPIO.LOW )

            GPIO.output( s2_i1, GPIO.LOW )
            GPIO.output( s2_i2, GPIO.LOW )
            GPIO.output( s2_i3, GPIO.LOW )
            GPIO.output( s2_i4, GPIO.LOW )
        else:
            servoX.stop()
            servoY.stop()

        GPIO.cleanup()

    def alarm():
        print(Fore.BLUE + "Alarm is sounding...")
        playsound('alarm.mp3', False)


    def to_servos(x, y):
        # Convert degrees to duty cycle
        x = (x/18) + 2.5
        y = (y/18) + 2.5
        
    def to_steppers(x, y):
        
        # Convert degrees to duty cycle
        x = (x/18) + 2.5
        y = (y/18) + 2.5

        x_degrees, x_clockwise = 0, True
        y_degrees, y_clockwise = 0, True

        x_motor_step_counter = 0
        y_motor_step_counter = 0
        
        for pin in range(0, len(motor_pinsX)):
            GPIO.output( motor_pinsX[pin], step_sequence[x_motor_step_counter][pin] )
        
        for pin in range(0, len(motor_pinsY)):
            GPIO.output( motor_pinsY[pin], step_sequence[y_motor_step_counter][pin] )

        if x_clockwise:
            for i in range(x_degrees):
                x_motor_step_counter = (x_motor_step_counter - 1) % 8
        elif not x_clockwise:
            for i in range(x_degrees):
                x_motor_step_counter = (x_motor_step_counter + 1) % 8

        if y_clockwise:
            for i in range(y_degrees):
                y_motor_step_counter = (y_motor_step_counter - 1) % 8
        elif not y_clockwise:
            for i in range(y_degrees):
                y_motor_step_counter = (y_motor_step_counter + 1) % 8

    def run(self, x, y, CAP_WIDTH, CAP_HEIGHT, CAP_WIDTH_VIEW_ERR, CAP_HEIGHT_VIEW_ERR):
    
        # Convert pixel coordinates to degrees
        x = map([0, CAP_WIDTH], [0, 180])
        y = map([0, CAP_HEIGHT], [0, 180])
        # Compensate for the camera's field of view
        
        # Horizontal Axis
        if x > CAP_WIDTH_VIEW_ERR and x < CAP_WIDTH - CAP_WIDTH_VIEW_ERR:
            pass
        elif x < CAP_WIDTH_VIEW_ERR:
            x = x + CAP_WIDTH_VIEW_ERR
        elif x > CAP_WIDTH - CAP_WIDTH_VIEW_ERR:
            x = x - CAP_WIDTH_VIEW_ERR
        
        # Vertical Axis
        if y > CAP_HEIGHT_VIEW_ERR and y < CAP_HEIGHT - CAP_HEIGHT_VIEW_ERR:
            pass
        elif y < CAP_HEIGHT_VIEW_ERR:
            y = y + CAP_HEIGHT_VIEW_ERR
        elif y > CAP_HEIGHT - CAP_HEIGHT_VIEW_ERR:
            y = y - CAP_HEIGHT_VIEW_ERR



        # convert vals and move turret

        if using_steppers:
            self.to_steppers(x, y)
        elif not using_steppers:
            self.to_servos(x, y)
        else:
            print("'using_steppers' not set!!!")
            exit

            