
from re import L
from tkinter import W
import random


class StimuliEfficacy:
    n_it_per_group: int
    stimuli: list
    motion_types: list
    actuators_list: dict  # 1-D tuple or 2-D tuples of actuators involved for each number 

    act_list = {
        'n_actuators': int, # number of actuators
        'width': list,  # list of <width, length>
        'length': list  # list of <width, length>
    }

    def __init__(self, nb_iteration_per_group):
        self.n_it_per_group = nb_iteration_per_group
        self.motion_types = []
        self.actuators_list = []
        self.stimuli = []

    def clear_all(self):
        self.motion_types.clear()
        self.actuators_list.clear()
        self.stimuli.clear()


    def define_types_motion(self):
        self.motion_types = ["rabbit", "app-motion"]

    def define_numbers(self):
        self.actuators_list = dict()
        # Load the actuators list for each number 
        self.actuators_list[0] = self.get_actuatorsList_for(0)
        self.actuators_list[1] = self.get_actuatorsList_for(1)
        self.actuators_list[2] = self.get_actuatorsList_for(2)
        self.actuators_list[3] = self.get_actuatorsList_for(3)
        self.actuators_list[4] = self.get_actuatorsList_for(4)
        self.actuators_list[5] = self.get_actuatorsList_for(5)
        self.actuators_list[6] = self.get_actuatorsList_for(6)
        self.actuators_list[7] = self.get_actuatorsList_for(7)
        self.actuators_list[8] = self.get_actuatorsList_for(8)
        self.actuators_list[9] = self.get_actuatorsList_for(9)
        
    def generate_set_stimuli(self, randomize=True):
        for number in self.actuators_list:
            actuators_engaged = self.actuators_list[number]
            
            if type(actuators_engaged[0]) == tuple:
            # it means the number implies a path larger than one actuator 
                w = len(actuators_engaged)
                l = len(actuators_engaged[0])
            else:
                w = 1
                l = len(actuators_engaged)
            n_act = w*l

            # save the pattern for each type of stimulation
            for t in self.motion_types:
                self.stimuli.append({
                        'type': t,
                        'nb_actuators': n_act,
                        'width': w,
                        'length': l,
                        'actuators': actuators_engaged
                })
        # randomize the stimuli
        if randomize:
            self.stimuli = random.sample(self.stimuli, len(self.stimuli))

    def get_actuatorsList_for(self, number):
        actuators : tuple
        if number == 0 :
            actuators = ("palm21", "palm33", "rf3")
        elif number == 1 :
            # if the number requires larger path than just one actuator-line, you can embed tuples within a tuple
            actuators = (("p1", "p2", "palm33"), ("rf3", "rf2", "palm11")) 
        elif number == 2 :
            actuators = ("palm21", "palm33", "rf3")
        elif number == 3 :
            actuators = ("palm21", "palm33", "rf3")
        elif number == 4 :
            actuators = ("palm21", "palm33", "rf3")
        elif number == 5 :
            actuators = ("palm21", "palm33", "rf3")
        elif number == 6 :
            actuators = ("palm21", "palm33", "rf3")
        elif number == 7 :
            actuators = ("palm21", "palm33", "rf3")
        elif number == 8 :
            actuators = ("palm21", "palm33", "rf3")
        elif number == 9 :
            actuators = ("palm21", "palm33", "rf3")

        return actuators

    def get_stimulus(self, stimulus_id):
        return self.stimuli[stimulus_id]

    def get_n_stimuli(self):
        return len(self.stimuli)

            










