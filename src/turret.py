from colorama import Fore
import time
import os
from serial import Serial
from playsound import playsound
import threading

alarm_file = "../assets/doom.mp3"

baud_rate = 9600
ard_tty = ""
if os.name == 'nt':
    ard_tty == 'COM14'
elif os.name == 'posix':
    ard_tty = '/dev/ttyACM0'

arduino = Serial(port='COM14', baudrate=baud_rate)


def fire(x, y):
    if arduino.isOpen():
        arduino.write(bytes(f'({x},{y})', 'utf-8'))
        #print(f'{Fore.GREEN}({x},{y}){Fore.RESET}')

def alarm():
    playsound(alarm_file)

def turret(x, y):
    t1 = threading.Thread(target=fire, args=(x, y))
    t1.start()
    # check if alarm thread exists
    if not any(t.name == 'alarm' for t in threading.enumerate()):
        t2 = threading.Thread(target=alarm, name='alarm')
        t2.start()