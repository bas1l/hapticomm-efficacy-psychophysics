#!/usr/bin/env python3

import os
import time
import random
import sys

# RASPBERRY PI 3 AND 4 AUTO-INSTALLATION ISSUE WITH QT4/5
# https://qengineering.eu/install-qt5-with-opencv-on-raspberry-pi-4.html
# https://raspberrypi.stackexchange.com/questions/69345/installing-qt-on-raspberry-pi-3
from datetime import datetime
import time
from time import sleep

from modules.stimuli import StimuliEfficacy
from modules.hapticomm_communication import HapticommSocket

import keyboard
script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_path)

global releaseListening
keepListening = True

# -- START COMMUNICATION WITH THE HAPTICOMM --
hapticomm = HapticommSocket()
hapticomm.initialise()

# -- SETUP STIMULUS CONTROL --
n_iteration_per_group = 1
s = StimuliEfficacy(n_iteration_per_group)
s.define_types_motion()
s.define_numbers()
s.generate_set_stimuli(randomize=False)

commands = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]

# -- ABORT/EXIT ROUTINE --
def key_press(key):
    print("key!")
    #if escape is pressed make listening false and exit 
    if key.name == "esc" or key.name == "r":
        keepListening = False
    elif key.name.lower() in commands:
        c = key.name.lower()
        if c == "0":
            stim = s.get_stimulus(0)
        elif c == "1":
            stim = s.get_stimulus(1)
        elif c == "2":
            stim = s.get_stimulus(2)
        elif c == "3":
            stim = s.get_stimulus(3)
        elif c == "4":
            stim = s.get_stimulus(4)
        elif c == "5":
            stim = s.get_stimulus(5)
        elif c == "6":
            stim = s.get_stimulus(6)
        elif c == "7":
            stim = s.get_stimulus(7)
        elif c == "8":
            stim = s.get_stimulus(8)
        elif c == "9":
            stim = s.get_stimulus(9)
        elif c == "q":
            stim = s.get_stimulus(10)
        elif c == "w":
            stim = s.get_stimulus(11)
        elif c == "e":
            stim = s.get_stimulus(12)
        elif c == "r":
            stim = s.get_stimulus(13)
        elif c == "t":
            stim = s.get_stimulus(14)
        elif c == "y":
            stim = s.get_stimulus(15)
        elif c == "u":
            stim = s.get_stimulus(16)
        elif c == "i":
            stim = s.get_stimulus(17)
        elif c == "o":
            stim = s.get_stimulus(18)
        elif c == "p":
            stim = s.get_stimulus(19)
            
        t = stim['type']
        width = stim['width']
        length = stim['length']
        actuators = stim['actuators']
        # send command to the AD5383
        print("\nPython: send ", t)
        hapticomm.send_pattern(t, width, length, actuators)
        sleep(1.0)


''' Description:
'''
if __name__ == '__main__':
    keyboard.on_press(key_press)   
    print("\n---")
    print("Press any number to display its tactile pattern")
    input("Enter r or <esq> to exit:\n")

    # -- MAIN EXPERIMENT LOOP --
    #sleep(0.5)  # let a bit of time for the AD5383 driver to start
    while keepListening:
        pass
                
        
        


