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


def get_random_edged_actuators(nmax_locations):
    # return nmax_locations number of random actuator identifiers.
    # It has to be an actuator on the edge of the device to facilitate the apparent motion

    act_neighbours = get_actuators_neighbours()
    actID = get_actuators_id()
    random.sample(actID, len(actID))

    actID_kept = [None] * nmax_locations
    n_locations = 0
    for a_id in actID:
        if is_contour(a_id):
            actID_kept[n_locations] = a_id
            n_locations += 1

        if n_locations == nmax_locations:
            return actID_kept

    return []


def is_contour(actuator_id):
    # at least one of the direction is None
    act_neighbours = get_actuators_neighbours()
    n = act_neighbours[actuator_id]
    return n["left"] is None or n["up"] is None or n["down"] is None or n["right"] is None


def get_random_lines(actIDs):
    # return a line of actuator identifiers for each actuator identifiers as input
    act_lines = []
    len_line_potential = [2, 3]

    for a_id in actIDs:
        random.shuffle(len_line_potential)
        act_line = None

        # get all the possible combination to get a line, exit as soon as found one.
        for n_act in len_line_potential:
            directions = ("left", "up", "down", "right")
            act_line = get_random_line(a_id, n_act, directions)
            if act_line is not None:
                break  # if a line has been found, then go to the next location.

        # If one of the starting actuators doesn't work, stops and returns nothing.
        if act_line is None:
            return None
        act_lines.append(act_line)

    return act_lines


def get_random_line(a_id_start, nb_act, directions):
    # return a line of actuator identifiers for the actuator identifier as input
    directions = random.sample(directions, len(directions))
    for d in directions:
        res = get_line(a_id_start, nb_act, d)
        if res is not None:
            return res, d  # a line has been found so it can exit.

    return None


def get_line(a_id_start, nb_act, direction):
    act_neighbours = get_actuators_neighbours()
    a_ids = [a_id_start]

    # store info of the first actuator [id and neighbours]
    neighbours = act_neighbours[a_id_start]

    # check if we can find a line
    for n_act in range(1, nb_act):
        n = neighbours[direction]
        if n is None:
            return None  # can't find the line, exit without returning anything.

        # save the actuator id in this direction
        if isinstance(n, list):  # therefore there are multiple choices, randomly chose one
            a_ids.append(random.sample(n, 1)[0])
        else:
            a_ids.append(n)

        neighbours = act_neighbours[a_ids[n_act]]  # jump to the neighbours of the next actuator

    return a_ids






