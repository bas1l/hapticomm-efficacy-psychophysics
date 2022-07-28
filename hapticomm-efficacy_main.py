#!/usr/bin/env python3

import os
import time
import random

from psychopy import core, data, gui
from pynput import keyboard

from modules.file_management import FileManager
from modules.stimuli import StimuliEfficacy

script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_path)

# -- GET INPUT FROM THE EXPERIMENTER --
expt_info = {
    '01. Experiment Name': 'hapticomm-efficacy-psychophysics',
    '02. Participant Code': 'P01',
    '03. Folder for saving data': 'data'
    }
dlg = gui.DlgFromDict(expt_info, title='Hapticomm Efficacy: psychophysics')
if dlg.OK:
    pass  # continue
else:
    core.quit()  # the user hit cancel so exit

# add the time when the user pressed enter:
date_time = data.getDateStr(format='%Y-%m-%d_%H-%M-%S')
experiment_name = expt_info['01. Experiment Name']
participant_id = expt_info['02. Participant Code']
data_folder = expt_info['03. Folder for saving data']

# -- MAKE FOLDER/FILES TO SAVE DATA --
filename_core = experiment_name + '_' + participant_id
filename_prefix = date_time + '_' + filename_core
fm = FileManager(data_folder+"/"+participant_id, filename_prefix)
fm.generate_infoFile(expt_info)

# -- SETUP STIMULUS CONTROL --
n_iteration_per_group = 10
s = StimuliEfficacy(n_iteration_per_group)
s.define_sizes()
s.define_stimuli()
n_trials = len(s.stim_list)

# -- SETUP EXPERIMENT CLOCKS --
expt_clock = core.Clock()
stim_clock = core.Clock()


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
stim_no = 0
expt_clock.reset()
fm.logEvent(expt_clock.getTime(), "experiment started")
while stim_no < n_trials:

    # pre-stimulus waiting period
    stim_clock.reset()
    while stim_clock.getTime() < 0.05:
        pass

    # write to data file
    fm.dataWrite([
        stim_no+1,
        s.stim_list[stim_no]['type'],
        s.stim_list[stim_no]['nb_actuators'],
        s.stim_list[stim_no]['width'],
        s.stim_list[stim_no]['length'],
        s.stim_list[stim_no]['actuators']
    ])

    # send command to the AD5383
    # TODO
    #  Execute the sequence
    #   - send the type of contact
    #   - send the list of actuators
    #  Wait for the participant's answer (one needs to press [Enter] to continue)

    fm.logEvent(
        expt_clock.getTime(),
        "stimulus {} of {} complete" .format(stim_no+1, n_trials)
    )
    stim_no += 1

fm.logEvent(expt_clock.getTime(), "Experiment finished")