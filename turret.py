from colorama import Fore
import time
import os
from serial import Serial

baud_rate = 9600
ard_tty = "COM"

if os.name == 'nt':
    ard_tty == 'COM14'
elif os.name == 'posix':
    ard_tty = '/dev/ttyACM0'

arduino = Serial(port='COM14', baudrate=baud_rate)

def fire(x, y):
    if arduino.isOpen():
        arduino.write(bytes(f'({x},{y})', 'utf-8'))
        #print(f'{Fore.GREEN}({x},{y}){Fore.RESET}')
