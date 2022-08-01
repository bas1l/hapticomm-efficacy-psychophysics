
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

    def clear_all(self):
        self.n_patterns.clear()
        self.stim_list.clear()

    def define_sizes(self):
        # The number 1 is ignored as slide cannot be done with one motor.
        # without the prime number 7, 11: Obviously, there are issues when grouping)
        for i in range(self.n_it_per_group):
            self.add_shape(random.choice([2, 3, 4]))  # small group
            self.add_shape(random.choice([5, 6, 8]))  # medium group
            self.add_shape(random.choice([9, 10, 12]))  # large group

    def add_shape(self, n_actuators):
        print("n_actuators: ", n_actuators)
        [n_actuators, w, l] = self.define_shape(n_actuators)
        self.n_patterns.append({'n_actuators': n_actuators, 'width': w, 'length': l})

    def define_shape(self, n_actuators):
        n_actuators_max = 12
        n_length_max = 6
        n_width_max = 4
        choices: list = []
        choice = None

        if not (1 < n_actuators <= n_actuators_max):
            raise Exception("The required number of actuators should be comprised between 2 and 12.")

        # check all dividend
        for dividend in range(1, n_length_max):
            # if the number of actuator can be split with integrity (no half-actuator on a line)
            if n_actuators%dividend == 0:
                w = int(n_actuators/dividend)
                # if the width is comprised within its limit:
                if w <= n_width_max:
                    l = dividend
                    choices.append([n_actuators, w, l])

        choice = random.sample(choices, 1)[0]
        return choice 
    
    def define_stimuli(self, randomize=True):
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
        if randomize:
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














