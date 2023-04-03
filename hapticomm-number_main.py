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

from pynput import keyboard
from time import sleep

from modules.file_management import FileManager
from modules.stimuli import StimuliEfficacy
from modules.hapticomm_communication import HapticommSocket

script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_path)

# -- START COMMUNICATION WITH THE HAPTICOMM --
hapticomm = HapticommSocket()
hapticomm.initialise()

# -- GET INPUT FROM THE EXPERIMENTER --
expt_info = {
    '01. Experiment Name': 'hapticomm-efficacy-psychophysics',
    '02. Participant Code': 'P00',
    '03. Folder for saving data': 'data'
    }

# add the time when the user pressed enter:
date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
experiment_name = expt_info['01. Experiment Name']
participant_id = expt_info['02. Participant Code']
data_folder = expt_info['03. Folder for saving data']
n_iteration_per_group = 10


# -- POTENTIAL ARGUMENT FOR THE PYTHON SCRIPT --
if len(sys.argv) > 1:
    participant_id = sys.argv[1]
if len(sys.argv) > 2:
    n_iteration_per_group = int(sys.argv[2])
    

# -- MAKE FOLDER/FILES TO SAVE DATA --
filename_core = experiment_name + '_' + participant_id
filename_prefix = date_time + '_' + filename_core
fm = FileManager(data_folder+"/"+participant_id, filename_prefix)
fm.generate_infoFile(expt_info)

# -- SETUP STIMULUS CONTROL --
s = StimuliEfficacy(n_iteration_per_group)
s.define_types_motion()
s.define_numbers()
s.generate_set_stimuli()
n_trials = s.get_n_stimuli()


# -- ABORT/EXIT ROUTINE --
def abort_experiment(key):
    if key == keyboard.Key.esc:
        fm.logEvent(expt_clock.getTime(), "experiment aborted")
        os._exit(0)


listener = keyboard.Listener(
    on_press=abort_experiment,
    on_release=abort_experiment)

listener.start()  # now the script will exit if you press escape


# -- MAIN EXPERIMENT LOOP --
sleep(0.5)  # let a bit of time for the AD5383 driver to start
stim_no = 0
start = time.time()
fm.logEvent(time.time()-start, "experiment started")
while stim_no < n_trials:
    # current stimulus information
    stim = s.get_stimulus(stim_no)
    motion_type = stim['type']
    n_act = stim['nb_actuators']
    width = stim['width']
    length = stim['length']
    actuators = stim['actuators']

    # write to data file
    fm.dataWrite([stim_no+1, motion_type, n_act, width, length, actuators])

    # send command to the AD5383
    #  Execute the sequence
    #   - send the type of contact
    #   - send the list of actuators
    #  Wait for the participant's answer (one needs to press [Enter] to continue)
    print("\n---")
    input("Press Enter to send a pattern...")
    print("\nPython: send_pattern")
    hapticomm.send_pattern(motion_type, width, length, actuators)
    sleep(0.75)

    fm.logEvent(
        time.time()-start,
        "stimulus {} of {} complete" .format(stim_no+1, n_trials)
    )
    stim_no += 1

fm.logEvent(time.time()-start, "Experiment finished")

hapticomm.close()
sleep(1)