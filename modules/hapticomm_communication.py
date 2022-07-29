
from multiprocessing import Process, Value
# The multiprocessing Queue class is a near clone of Queue.Queue (https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Queue)
from multiprocessing import Queue
# Necessary to handle Empty exceptions (https://stackoverflow.com/questions/6491942/cannot-access-queue-empty-attributeerror-function-object-has-no-attribute)
from queue import Empty

import pathlib
import subprocess

# socket communication
import zmq

SIG_END_PROGRAM = b'SIG_END_PROGRAM'  # defined in the hapticomm driver


def format_actuators_line(actuators):
    instruction = ""
    first = True
    for a in actuators:
        if first:
            first = False
        else:
            instruction += ","
        instruction += a

    return instruction


def format_stimulus(motion, width, length, actuators):
    instruction = motion + ";" + str(width) + ";" + str(length)
    if width == 1:
        instruction += ";" + format_actuators_line(actuators)
    else:
        # for each width line
        for ll in actuators:
            instruction += ";" + format_actuators_line(ll)
    instruction += "\n"
    return instruction


class HapticommSocket:

    def __init__(self, local_path="/../build/bin/"):
        self.hapticommDriver_path = str(pathlib.Path(__file__).parent.resolve()) + local_path
        self.p_act_driver = None

    def __del__(self):
        self.close()

    def initialise(self):
        self.neutral()  # initialise the apparatus to neutral
        self.p_act_driver = Process(target=self.start_hapticomm_driver)
        self.p_act_driver.start()

        #  Socket to talk to server
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5556")

    # Ensure the resting state (0V) of the actuators
    def neutral(self):
        subprocess.run([self.hapticommDriver_path + "neutral"])

    # AD3583 driver listening to the socket 5556
    def start_hapticomm_driver(self):
        command = self.hapticommDriver_path + "listener_AD5383"
        subprocess.run([command])

    def send_pattern(self, motion, width, length, actuators):
        instruction = format_stimulus(motion, width, length, actuators)
        self.socket.send(instruction.encode('utf-8'))

    def close(self):
        self.socket.send(SIG_END_PROGRAM)