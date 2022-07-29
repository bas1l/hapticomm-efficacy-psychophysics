
from modules.include.actuators_info import *
import random


class StimuliEfficacy:
    stim_list: list
    stim_types: list
    n_it_per_group: int
    neighbours: list
    actuators: list
    n_patterns = {
        'small': list,   # 2-4 actuators  :  list of n_shape type
        'medium': list,  # 5-8 actuators  :  list of n_shape type
        'large': list    # 9-12 actuators :  list of n_shape type
    }
    n_shape = {
        'n_actuators': int, # number of actuators
        'width': list,  # list of [width, length]
        'length': list  # list of [width, length]
    }

    def __init__(self, nb_iteration_per_group):
        self.n_it_per_group = nb_iteration_per_group
        self.neighbours = get_actuators_neighbours()
        self.actuators = get_actuators_id()
        self.directions = get_directions()
        self.stim_types = ["tap", "tap-and-hold", "slide"]

        self.n_patterns['small'] = []
        self.n_patterns['medium'] = []
        self.n_patterns['large'] = []

        self.stim_list = []

    def get_random_actuators(self, nmax_locations):
        return random.sample(self.actuators, nmax_locations)

    def define_sizes(self):
        # without the prime number 1, 7, 11: Obviously, there are issues when grouping)

        # Small condition (2-4)
        for i in range(self.n_it_per_group):
            n_actuators = random.choice([2, 3, 4])
            if n_actuators == 4 and random.choice([True, False]):
                # can be a square with 4 actuators.
                w, l = [2, 2]
            else:
                w, l = [1, n_actuators]
            shape = {
                'n_actuators': n_actuators,
                'width': w,
                'length': l
            }
            self.n_patterns['small'].append(shape)

        # Medium condition (5-8)
        for i in range(self.n_it_per_group):
            n_actuators = random.choice([5, 6, 8])
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

            shape = {
                'n_actuators': n_actuators,
                'width': w,
                'length': l
            }
            self.n_patterns['medium'].append(shape)

        # Large condition (5-8)
        for i in range(self.n_it_per_group):
            n_actuators = random.choice([9, 10, 12])
            if n_actuators == 9:
                w, l = [3, 3]
            elif n_actuators == 10:
                w, l = [2, 5]
            elif n_actuators == 12:
                if random.choice([True, False]):
                    w, l = [3, 4]
                else:
                    w, l = [4, 3]

            shape = {
                'n_actuators': n_actuators,
                'width': w,
                'length': l
            }
            self.n_patterns['large'].append(shape)

    def define_stimuli(self):
        for pk, pv in self.n_patterns.items():
            for v in pv:
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