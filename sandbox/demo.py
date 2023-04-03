#!/usr/bin/env python

''' Description:
Converts vibrations from accelerometers to vibrotactile actuators behaviors in real time
1. each accelerometer is associated to an actuator
2. only the Z-axis is taken into account
3. digest Z-axis values into actuator behavior
'''
# usage:
#   python demo.py 

from ast import arg
from colorama import Fore
from datetime import datetime
from multiprocessing.connection import wait
from urllib.parse import parse_qs

import math
import numpy as np
import serial
import shlex
import subprocess
import sys
import time
import pathlib
import zmq
import colorama

from multiprocessing import Process, Value
# The multiprocessing Queue class is a near clone of Queue.Queue (https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Queue)
from multiprocessing import Queue
# Necessary to handle Empty exceptions (https://stackoverflow.com/questions/6491942/cannot-access-queue-empty-attributeerror-function-object-has-no-attribute)
from queue import Empty

import sys
sys.path.append('../../modules')
from ActuLine import ActuLine, Actuator


class States:
    is_collecting : Value('b', True)
    is_comm_ready : Value('b', False)


# Ensure the resting state (0V) of the actuators
def neutral(ad5383_path):
    subprocess.run([ad5383_path + "neutral"])


# AD3583 driver listening to the socket 5556
def start_actuators_driver(ad5383_path):
    subprocess.run([ad5383_path + "listener_AD5383"])


def initialise_actuators(socket, aL):
    chan = aL.get_dacChannels()
    instruction = "dacChannels:"+ chan[0] +","+ chan[1] +","+ chan[2] +","+ chan[3] +","+ chan[4] +","+ chan[5] +"\n" 
    socket.send(instruction.encode('utf-8'))
    instruction = "frequency:" + aL.get_freqRefresh() + "\n" # in Hz
    socket.send(instruction.encode('utf-8'))



def interpret(socket,  aL):
    m = aL.define_trajectories(m)
    instruction = str(1)+","\
                + str(m[0]) +"," \
                + str(m[1]) +"," \
                + str(m[2]) +"," \
                + str(m[3]) +"," \
                + str(m[4]) +"," \
                + str(m[5]) +"\n"
    socket.send(instruction.encode('utf-8'))

    for i in range(10): 
        socket.send(b'0,2048,2048,2048,2048,2048,2048\n')
    socket.send(b'SIG_END_PROGRAM')




''' Description:
'''
if __name__ == '__main__':
    #  Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")

    # Get configuration from config file
    aL = ActuLine("../../cfg/config.json")
    aL.configure()

    # AD5383 driver initialisation
    print ("Main: Start the communication with the actuators.")
    script_directory = str(pathlib.Path(__file__).parent.resolve())
    ad5383_path = script_directory + "/../../../AD5383_driver/build/bin/"
    neutral(ad5383_path)
    p_act_driver = Process(target=start_actuators_driver, args=(ad5383_path,))
    p_act_driver.start()

    time.sleep(1) # let some time to the AD5383 driver to set up the socket; it must be done with a duplex socket
    initialise_actuators(socket, aL)

    input ("---[Press Start to begin the demo]---")
    print ("Main: Start reading the accelerometers...")   
    if len(sys.argv) == 2: 
        end_working_sec = time.process_time()+ int(sys.argv[1]) # now+X seconds
    else: 
        end_working_sec = time.process_time()+ 5 # now+X seconds

    interpret(socket, aL)

    p_act_driver.join()
    print ("Main: Close the communication with the actuators.")
    teensy_ser.close()  # Close the USB port and pipe
    print ("Main: Close the communication with the Teensy/accelerometers.")    

    print ("Main: ends.")

    