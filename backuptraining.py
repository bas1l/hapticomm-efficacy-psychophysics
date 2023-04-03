
from re import L
from tkinter import W
from modules.include.actuators_info import *
import random


class StimuliEfficacy:
    stim_list: list
    stim_types: list
    n_it_per_group: int
    neighbours: list
    actuators: list
    n_patterns: list   # list of <n_shape type>
    n_shape = {
        'n_actuators': int, # number of actuators
        'width': list,  # list of <width, length>
        'length': list  # list of <width, length>
    }

    def __init__(self, nb_iteration_per_group):
        self.n_it_per_group = nb_iteration_per_group
        self.neighbours = get_actuators_neighbours()
        self.actuators = get_actuators_id()
        self.directions = get_directions()
        self.stim_types = ["tap", "tap-and-hold", "slide"]

        self.n_patterns = []

        self.stim_list = []

    def get_random_actuators(self, nmax_locations):
        return random.sample(self.actuators, nmax_locations)

    def define_sizes(self):
        # The number 1 is ignored as slide cannot be done with one motor.
        # without the prime number 7, 11: Obviously, there are issues when grouping)
        for i in range(self.n_it_per_group):
            self.add_shape(random.choice([2, 3, 4]))  # small group
            self.add_shape(random.choice([5, 6, 8]))  # medium group
            self.add_shape(random.choice([9, 10, 12]))  # large group

    # Small condition (2-4)
    def add_shape_small(self, n_actuators):
        n_actuators, w, l = self.define_shape_small(n_actuators)
        self.add_shape(n_actuators, w, l)

    # Medium condition (5-8)
    def add_shape_medium(self, n_actuators):
        n_actuators, w, l = self.define_shape_medium(n_actuators)
        self.add_shape(n_actuators, w, l)

    # Large condition (9-12)
    def add_shape_large(self, n_actuators):
        n_actuators, w, l = self.define_shape_large(n_actuators)
        self.add_shape(n_actuators, w, l)
    
    def add_shape(self, n_actuators):
        n_actuators, w, l = self.define_shape(n_actuators)
        self.n_patterns.append({'n_actuators': n_actuators, 'width': w, 'length': l})

    def define_shape(self, n_actuators):
        n_actuators_max = 12
        n_length_max = 6
        n_width_max = 4
        choices: list = []

        if not (1 < n_actuators <= n_actuators_max):
            raise Exception("The required number of actuators should be comprised between 2 and 12.")

        # check all dividend
        for dividend in range(1, n_length_max):
            # if the number of actuator can be split with integrity (no half-actuator on a line)
            if n_actuators%dividend == 0:
                w = n_actuators/dividend
                # if the width is comprised within its limit:
                if w <= n_width_max:
                    l = dividend
                    choices.append([n_actuators, w, l])

        return random.sample(choices, 1)
    
    # Small condition (2-4)
    def define_shape_small(self, n_actuators):
        if n_actuators == 4 and random.choice([True, False]):
            # can be a square with 4 actuators.
            w, l = [2, 2]
        else:
            w, l = [1, n_actuators]
        return n_actuators, w, l

    # Medium condition (5-8)
    def define_shape_medium(self, n_actuators):
        if n_actuators == 5:
            w, l = [1, n_actuators]
        elif n_actuators == 8:
            if random.choice([True, False]):
                w, l = [2, 4]
            else:
                w, l = [4, 2]
        elif n_actuators == 6:
            c = random.choice([1, 2, 3])
            if c == 1:
                w, l = [1, n_actuators]
            elif c == 2:
                w, l = [2, 3]
            elif c == 3:
                w, l = [3, 2]
        return n_actuators, w, l

    # Large condition (9-12)
    def define_shape_large(self, n_actuators):
        if n_actuators == 9:
            w, l = [3, 3]
        elif n_actuators == 10:
            w, l = [2, 5]
        elif n_actuators == 12:
            if random.choice([True, False]):
                w, l = [3, 4]
            else:
                w, l = [4, 3]
        return n_actuators, w, l

    def add_shape(self, n_actuators, width, length):
        shape = {
            'n_actuators': n_actuators,
            'width': width,
            'length': length
        }
        self.n_patterns.append(shape)

    def define_stimuli(self):
        for v in self.n_patterns:
            n_act = v['n_actuators']
            w = v['width']
            l = v['length']

            if w == 1:
                actuators_list = self.get_path(l)
            else:
                actuators_list = self.get_path_large(w, l)

            # save the pattern for each type of stimulation
            for t in self.stim_types:
                self.stim_list.append({
                        'type': t,
                        'nb_actuators': n_act,
                        'width': w,
                        'length': l,
                        'actuators': actuators_list
                })
        # randomize the stimuli
        self.stim_list = random.sample(self.stim_list, len(self.stim_list))

    def get_path(self, length):
        path = []
        done = False
        while not done:
            path = []
            n_actuators = 0
            a = random.sample(self.actuators, 1)[0]  # select a random starting point

            while a is not None and not (a in path):
                path.append(a)
                n_actuators += 1
                if n_actuators == length:
                    done = True
                    break
                else:
                    d = random.sample(self.directions, 1)[0]
                    a = self.neighbours[a][d]  # targeted neighbour
                    # duplicate necessary for the first check
                    if isinstance(a, list):  # there are multiple choices, randomly chose one
                        a = random.sample(a, 1)[0]
        return path

    def get_path_large(self, width, length):
        dir_vert = get_directions_vertical()
        dir_hor = get_directions_horizontal()

        done = False
        while not done:
            a = random.sample(self.actuators, 1)[0]  # select a random starting point
            line_width, dir_width = get_random_line(a, width, self.directions)
            # if a line has been found
            if len(line_width):
                if dir_width in dir_vert:
                    l_slide, d_motion = get_large_slide(line_width, dir_width, dir_hor, length)
                else:
                    l_slide, d_motion = get_large_slide(line_width, dir_width, dir_vert, length)
                # if a path has been found
                if len(l_slide):
                    return l_slide

    def get_stimulus(self, stimulus_id):
        return self.stim_list[stimulus_id]

    def get_n_stimuli(self):
        return len(self.stim_list)
















def abort_experiment(key):
    if key == keyboard.Key.esc:
        #hapticomm.close()
        #sleep(1)
        os._exit(0)


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


#listener = keyboard.Listener(on_press=on_press, on_release=on_release)
#listener.start()  # now the script will exit if you press escape
#listener.join() 









#!/usr/bin/env python3

import keyboard
import os
import time
import random
import sys

# RASPBERRY PI 3 AND 4 AUTO-INSTALLATION ISSUE WITH QT4/5
# https://qengineering.eu/install-qt5-with-opencv-on-raspberry-pi-4.html
# https://raspberrypi.stackexchange.com/questions/69345/installing-qt-on-raspberry-pi-3
from datetime import datetime
import time

#from pynput import keyboard
from time import sleep

from modules.stimuli import StimuliEfficacy
from modules.hapticomm_communication import HapticommSocket

script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_path)

global releaseListening
keepListening = True


# -- SETUP STIMULUS CONTROL --
#hapticomm = HapticommSocket()
n_iteration_per_group = 1
s = StimuliEfficacy(n_iteration_per_group)
s.define_sizes()
s.define_stimuli()


# -- ABORT/EXIT ROUTINE --
def key_press(key):
    print(key.name)
    #if escape is pressed make listening false and exit 
    if key.name == "esc":
        keepListening = False

def print_command_info():
    print("\n---")
    print("To display a stimulus, press:")
    print("\t<q> for tap")
    print("\t<a> for tap-and-hold")
    print("\t<z> for slide.")
    print("To change the size of the stimulus: enter a number between 2 and 12.")
    

# current stimulus information
#stim = s.get_stimulus(1)
#t = stim['type']
#n_act = stim['nb_actuators']
#width = stim['width']
#length = stim['length']
#actuators = stim['actuators']
# send command to the AD5383
#print("\nPython: send_pattern")
#hapticomm.send_pattern(t, width, length, actuators)
#sleep(0.75)

''' Description:
'''
if __name__ == '__main__':

    # -- START COMMUNICATION WITH THE HAPTICOMM --
    #hapticomm = HapticommSocket()
    #hapticomm.initialise()


    commands = ["q", "a", "z"]
    
    keyboard.on_press(key_press)   

    # -- MAIN EXPERIMENT LOOP --
    #sleep(0.5)  # let a bit of time for the AD5383 driver to start
    while keepListening:
        pass
        # send command to the AD5383
        #print_command_info()
        #i = input("Press Enter to validate the command: ").lower()
        #if i.isnumeric() and 1 < int(i) <= 12:
        #    s.clear_all()
        #    s.add_shape(int(i))
        #    s.define_stimuli(randomize=False)
        
        



