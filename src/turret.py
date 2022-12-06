from colorama import Fore
import time
import os
from serial import Serial
from playsound import playsound
import threading

alarm_file = "../assets/owl.mp3"

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

def run(x, y):
    t1 = threading.Thread(target=fire, args=(x, y))
    t2 = threading.Thread(target=alarm)
    t1.start()
    # check if alarm thread is alive
    if not t2.is_alive():
        t2.start()