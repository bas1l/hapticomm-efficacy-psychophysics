import random
import numpy as np


# Just a file to define neighbour for each actuator
# to not take space in the main python script.
def get_actuators_neighbours():
    act_neighbours = {}

    # -- Thumb
    neighbours = {
        "left": "palm32",
        "up": None,
        "down": None,
        "right": "t2"
    }
    act_neighbours["t1"] = neighbours
    neighbours = {
        "left": "t1",
        "up": None,
        "down": None,
        "right": None
    }
    act_neighbours["t2"] = neighbours

    # -- Fore finger
    neighbours = {
        "left": "mf1",
        "up": "ff2",
        "down": "palm33",
        "right": None
    }
    act_neighbours["ff1"] = neighbours
    neighbours = {
        "left": "mf2",
        "up": "ff3",
        "down": "ff1",
        "right": None
    }
    act_neighbours["ff2"] = neighbours
    neighbours = {
        "left": "mf3",
        "up": None,
        "down": "ff2",
        "right": None
    }
    act_neighbours["ff3"] = neighbours

    # -- Middle Finger
    neighbours = {
        "left": "rf1",
        "up": "mf2",
        "down": ["palm33", "palm23"],
        "right": "ff1"
    }
    act_neighbours["mf1"] = neighbours
    neighbours = {
        "left": "rf2",
        "up": "mf3",
        "down": "mf1",
        "right": "ff2"
    }
    act_neighbours["mf2"] = neighbours
    neighbours = {
        "left": "rf3",
        "up": None,
        "down": "mf2",
        "right": "ff3"
    }
    act_neighbours["mf3"] = neighbours

    # -- Ring Finger
    neighbours = {
        "left": "p1",
        "up": "rf2",
        "down": ["palm13", "palm23"],
        "right": "mf1"
    }
    act_neighbours["rf1"] = neighbours
    neighbours = {
        "left": "p2",
        "up": "rf3",
        "down": "rf1",
        "right": "mf2"
    }
    act_neighbours["rf2"] = neighbours
    neighbours = {
        "left": None,
        "up": None,
        "down": "rf2",
        "right": "mf3"
    }
    act_neighbours["rf3"] = neighbours

    # -- Pinky
    neighbours = {
        "left": None,
        "up": "p2",
        "down": "palm13",
        "right": "rf1"
    }
    act_neighbours["p1"] = neighbours
    neighbours = {
        "left": None,
        "up": None,
        "down": "p1",
        "right": "rf2"
    }
    act_neighbours["p2"] = neighbours

    # -- Palm Column 1
    neighbours = {
        "left": None,
        "up": "palm12",
        "down": None,
        "right": "palm21"
    }
    act_neighbours["palm11"] = neighbours
    neighbours = {
        "left": "s1",
        "up": "palm13",
        "down": "palm11",
        "right": "palm22"
    }
    act_neighbours["palm12"] = neighbours
    neighbours = {
        "left": None,
        "up": ["p1", "rf1"],
        "down": "palm12",
        "right": "palm23"
    }
    act_neighbours["palm13"] = neighbours

    # -- Palm Column 2
    neighbours = {
        "left": "palm11",
        "up": "palm22",
        "down": "b1",
        "right": "palm31"
    }
    act_neighbours["palm21"] = neighbours
    neighbours = {
        "left": "palm12",
        "up": "palm23",
        "down": "palm21",
        "right": "palm32"
    }
    act_neighbours["palm22"] = neighbours
    neighbours = {
        "left": "palm13",
        "up": ["rf1", "mf1"],
        "down": "palm22",
        "right": "palm33"
    }
    act_neighbours["palm23"] = neighbours

    # -- Palm Column 3
    neighbours = {
        "left": "palm21",
        "up": "palm32",
        "down": "b1",
        "right": None
    }
    act_neighbours["palm31"] = neighbours
    neighbours = {
        "left": "palm22",
        "up": "palm33",
        "down": "palm31",
        "right": "t1"
    }
    act_neighbours["palm32"] = neighbours
    neighbours = {
        "left": "palm23",
        "up": ["mf1", "ff1"],
        "down": "palm32",
        "right": None
    }
    act_neighbours["palm33"] = neighbours

    # Bottom and Side
    neighbours = {
        "left": None,
        "up": ["palm21", "palm31"],
        "down": None,
        "right": None
    }
    act_neighbours["b1"] = neighbours
    neighbours = {
        "left": None,
        "up": None,
        "down": None,
        "right": "palm12"
    }
    act_neighbours["s1"] = neighbours

    return act_neighbours


def get_directions():
    return ["left", "up", "down", "right"]


def get_directions_horizontal():
    return ["left", "right"]


def get_directions_vertical():
    return ["up", "down"]


def get_actuators_id():
    actuators_id = ['t1', 't2',
                    'ff1', 'ff2', 'ff3',
                    'mf1', 'mf2', 'mf3',
                    'rf1', 'rf2', 'rf3',
                    'p1', 'p2',
                    'palm11', 'palm12', 'palm13',
                    'palm21', 'palm22', 'palm23',
                    'palm31', 'palm32', 'palm33',
                    'b1', 's1']

    return actuators_id


def get_random_lines(actIDs, directions=("left", "up", "down", "right")):
    # return a line of actuators for each actuator identifiers as input
    act_lines = []
    len_line_potential = [2, 3]

    for a_id in actIDs:
        random.shuffle(len_line_potential)
        act_line = None

        # get all the possible combination to get a line, exit as soon as found one.
        for n_act in len_line_potential:
            act_line = get_random_line(a_id, n_act, directions)[0]
            # if a line has been found, then go to the next location.
            if act_line is not None:
                break

        # If one of the starting actuators doesn't work, stops and returns nothing.
        if act_line is None:
            return None
        act_lines.append(act_line)

    return act_lines


def get_random_line(a_id_start, width, directions):
    directions = random.sample(directions, len(directions))
    # return a line of actuator identifiers for the actuator identifier as input
    for d in directions:
        res = get_line_limit(a_id_start, d, width)
        if res:
            return res, d  # a line has been found so it can exit.

    return [], None


def get_line_limit(a_id_start, direction, nb_act):
    # check if we can find a line
    line = get_line(a_id_start, direction)
    if isinstance(line, list) and len(line) >= nb_act:
        return line[0:nb_act]

    return []


def get_line(a_id_start, direction):
    line = [a_id_start]

    act_neighbours = get_actuators_neighbours()  # get the list of all neighbours
    neighbours = act_neighbours[a_id_start]  # neighbours of the current actuator
    n = neighbours[direction]  # targeted neighbour

    # While there is still actuators on the line
    while n is not None:
        if isinstance(n, list):  # there are multiple choices, randomly chose one
            line.append(random.sample(n, 1)[0])
        else:
            line.append(n)
        # select the next actuator and neighbours
        n = act_neighbours[line[-1]][direction]  # jump to the neighbours of the next actuator

    return line


def get_large_slide(acts_start, neighbours_dir, directions=("up", "down"), length=3):
    width = len(acts_start)
    directions = random.sample(directions, len(directions))

    for d in directions:
        used_actuators = []
        lines = []
        n_line = 0

        # starts by getting the line for one actuator and check if the width can be satisfied
        line = get_line(acts_start[0], d)
        for a in line:
            # check if the required width can be satisfied
            new_line = get_line(a, neighbours_dir)

            # if it contains an already used actuator, exit
            if any(item in new_line for item in used_actuators):
                break
            else:
                used_actuators.extend(new_line)

            # if the line is correct, add the line and go next
            if isinstance(new_line, list) and len(new_line) >= width:
                lines.append(new_line[0:width])
                n_line += 1
            # if not and minimum length not satisfied, go to the next direction
            else:
                break

            # if the minimum length is satisfied, stops searching.
            if n_line == length:
                return lines, d

    return [], None
