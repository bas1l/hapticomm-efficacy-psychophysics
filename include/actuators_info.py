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


def get_random_actuators(nmax_locations):
    actID = get_actuators_id()
    return random.sample(actID, nmax_locations)


def get_random_edged_actuators(nmax_locations):
    # return nmax_locations number of random actuator identifiers.
    # It has to be an actuator on the edge of the device to facilitate the apparent motion

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

    return None


def is_contour(actuator_id):
    # at least one of the direction is None
    act_neighbours = get_actuators_neighbours()
    n = act_neighbours[actuator_id]
    return n["left"] is None or n["up"] is None or n["down"] is None or n["right"] is None


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


def get_random_line(a_id_start, nb_act, directions):
    directions = random.sample(directions, len(directions))
    # return a line of actuator identifiers for the actuator identifier as input
    for d in directions:
        res = get_line_limit(a_id_start, d, nb_act)
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


def get_tap_stimuli(n_sequence):
    points = get_random_actuators(n_sequence)
    lines = get_random_lines(get_random_actuators(n_sequence))

    return [points, lines]


def get_points_slide(n_sequence):
    actuators = get_actuators_id()
    actuators = random.sample(actuators, len(actuators))

    lines = []
    n_found = 0

    for a in actuators:
        line, d = get_point_slide(a)
        if len(line):  # if not empty, line has been found
            lines.append([line, d])
            n_found += 1
        if n_found == n_sequence:
            break

    return lines


def get_point_slide(act_start):
    minimum_len = 3
    directions = ("up", "down")
    directions = random.sample(directions, len(directions))

    for d in directions:
        line = get_line(act_start, d)
        if isinstance(line, list) and len(line) >= minimum_len:
            return line, d

    return [], None


def get_lines_slide(n_sequence):
    matrix = []
    n_lines = 0

    actuators = get_actuators_id()
    len_line_potential = [2, 3]
    directions = ("left", "right")  # always horizontal as the motion is vertical

    while n_lines != n_sequence:
        nb_act = random.sample(len_line_potential, 1)[0]
        a = random.sample(actuators, 1)[0]
        line_width, d_width = get_random_line(a, nb_act, directions)
        # if a line has been found
        if len(line_width):
            l_slide, d_motion = get_large_slide(line_width, d_width)
            if len(l_slide):
                matrix.append([l_slide, d_motion])
                n_lines += 1

    return matrix


def get_large_slide(acts_start, neighbours_dir):
    width = len(acts_start)
    minimum_len = 3
    directions = ("up", "down")
    directions = random.sample(directions, len(directions))

    for d in directions:
        lines = []
        n_line = 0

        # starts by getting the line for one actuator and check if the width can be satisfied
        line = get_line(acts_start[0], d)
        for a in line:
            # check if the required width can be satisfied
            line_width = get_line(a, neighbours_dir)
            # if yes, add the line and go next
            if isinstance(line_width, list) and len(line_width) >= width:
                lines.append(line_width[0:width])
                n_line += 1
            # if not and minimum length not satisfied, go to the next direction
            else:
                break

        # if the minimum length was satisfied, stops searching.
        if n_line >= minimum_len:
            return lines, d

    return [], None


def get_stimuli(n_iteration_per_group):
    stim_list = []

    [points, lines] = get_tap_stimuli(n_iteration_per_group)
    for t in ['tap', 'tap-and-hold']:
        for point in points:
            stim_list.append({
                'type': t,
                'size': 'point',
                'direction': "None",
                'actuators': point
            })
        for line in lines:
            stim_list.append({
                'type': t,
                'size': 'line',
                'direction': "None",
                'actuators': line
            })

    lines = get_points_slide(n_iteration_per_group)
    for line, direction in lines:
        stim_list.append({
            'type': "app-motion",
            'size': 'point',
            'direction': direction,
            'actuators': line
        })
    matrices = get_lines_slide(n_iteration_per_group)
    for matrix, direction in matrices:
        stim_list.append({
            'type': "app-motion",
            'size': 'line',
            'direction': direction,
            'actuators': matrix
        })

    return stim_list

