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
s.add_shape(3) 
s.define_stimuli(randomize=False)

commands = ["q", "a", "z"]

# -- ABORT/EXIT ROUTINE --
def key_press(key):
    #if escape is pressed make listening false and exit 
    if key.name == "esc" or key.name == "r":
        keepListening = False
    elif key.name.lower() in commands:
        c = key.name.lower()
        if c == "q":
            stim = s.get_stimulus(0)
        elif c == "a":
            stim = s.get_stimulus(1)
        elif c == "z":
            stim = s.get_stimulus(2)
            
        t = stim['type']
        n_act = stim['nb_actuators']
        width = stim['width']
        length = stim['length']
        actuators = stim['actuators']
        # send command to the AD5383
        print("\nPython: send ", t)
        hapticomm.send_pattern(t, width, length, actuators)
        sleep(1.0)

def print_command_info():
    print("\n---")
    print("To display a stimulus, press:")
    print("\t<q> for tap")
    print("\t<a> for tap-and-hold")
    print("\t<z> for slide.")
    print("To change the size of the stimulus: Press [Enter], put a number between 2 and 12, then press [Enter] again.")
    print("To exit, press <r>.")
    print("---")
    

''' Description:
'''
if __name__ == '__main__':

    nb_act = 3
    keyboard.on_press(key_press)   

    # -- MAIN EXPERIMENT LOOP --
    #sleep(0.5)  # let a bit of time for the AD5383 driver to start
    while keepListening:
        pass
        # send command to the AD5383
        print_command_info()
        i = input("Enter another number of actuators (currently " + str(nb_act) + "): ").lower()
        if i.isnumeric() and 1 < int(i) <= 12:
            nb_act = int(i)
            s.clear_all()
            s.add_shape(nb_act)
            s.define_stimuli(randomize=False)
        
        


