#!/usr/bin/env python3
import random

from modules.stimuli import StimuliEfficacy
from modules.hapticomm_communication import HapticommSocket, format_stimulus


def stimuliEfficacy_tests(n=0):
    if n == 1:
        s = StimuliEfficacy(10)
        s.define_sizes()
        for p in s.n_patterns.values():
            for v in p:
                print(v)
        print( len( list(s.n_patterns.values())[0] ) )
    elif n == 2:
        s = StimuliEfficacy(10)
        s.define_sizes()
        s.define_stimuli()
        pass
    elif n == 3:
        s = StimuliEfficacy(3)
        s.define_sizes()
        s.define_stimuli()
    elif n == 4:
        s = StimuliEfficacy(10)
        s.define_sizes()
        s.define_stimuli()
        for stim in s.stim_list:
            print(stim)


def hapticommSocket_tests(n=0):
    if n == 1:
        #hsocket = HapticommSocket()
        s = StimuliEfficacy(3)
        s.define_sizes()
        s.define_stimuli()
        for n in range(s.get_n_stimuli()):
            stimulus = s.get_stimulus(n)
            print("---")
            print(stimulus)
            instruction = format_stimulus(stimulus['type'], stimulus['width'], stimulus['length'], stimulus['actuators'])
            print(instruction.encode('utf-8'))
    elif n == 2:
        pass


if __name__ == '__main__':
    hapticommSocket_tests(1)
    # stimuliEfficacy_tests(1)
    # stimuliEfficacy_tests(2)
    # stimuliEfficacy_tests(3)
    # stimuliEfficacy_tests(4)
