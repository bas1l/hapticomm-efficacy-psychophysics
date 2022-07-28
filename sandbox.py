#!/usr/bin/env python3
import random

from modules.stimuli import StimuliEfficacy

tests = 4

if tests == 1:
    s = StimuliEfficacy(10)
    s.define_sizes()
    for p in s.n_patterns.values():
        for v in p:
            print(v)
    print( len( list(s.n_patterns.values())[0] ) )
elif tests == 2:
    s = StimuliEfficacy(10)
    s.define_sizes()
    s.define_stimuli()
    pass
elif tests == 3:
    s = StimuliEfficacy(3)
    s.define_sizes()
    s.define_stimuli()
elif tests == 4:
    s = StimuliEfficacy(10)
    s.define_sizes()
    s.define_stimuli()
    for stim in s.stim_list:
        print(stim)
elif tests == 5:
    pass
elif tests == 6:
    pass