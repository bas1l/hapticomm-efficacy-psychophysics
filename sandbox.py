#!/usr/bin/env python3

from include.actuators_info import *
import random

points = get_random_edged_actuators(10)
# print(points)

directions = ("left", "up", "down", "right")
directions = random.sample(directions, len(directions))


tests = 10

if tests == 1:
    a_id_start = "p1"
    print(get_random_line(a_id_start, 2, directions)[0])
    print(get_random_line(a_id_start, 2, directions)[0:2])
elif tests == 2:
    sub_points = ["palm13", "palm23", "palm33"]
    lines = get_random_lines(sub_points)
    print(lines)
elif tests == 3:
    lines = get_random_lines(points)
    for ll in lines:
        print(ll)
elif tests == 4:
    contact_types = ['tap', 'tap-and-hold']
    contact_sizes = ['medium', 'large']
    n_iteration_per_stim = 10

    [points, lines] = get_tap_stimuli(n_iteration_per_stim)

    stim_list = []
    for t in contact_types:
        for point in points:
            stim_list.append({
                'type': t,
                'size': 'point',
                'actuators': point
            })
        for line in lines:
            stim_list.append({
                'type': t,
                'size': 'line',
                'actuators': line
            })
    #random.shuffle(stim_list)
    for s in stim_list:
        print(s)

elif tests == 5:
    directions = ("left", "up", "down", "right")
    for d in directions:
        print(get_line("palm22", d))
    for d in directions:
        print(get_line("t2", d))

elif tests == 6:
    lines = get_points_slide(10)
    for ll in lines:
        print(ll)

elif tests == 7:
    #acts_start = ["palm31", "palm21", "palm11"]
    acts_start = ["palm33", "palm23", "palm13"]
    neighbours_dir = "left"
    lines = get_large_slide(acts_start, neighbours_dir)
    for ll in lines:
        print(ll)

elif tests == 8:
    stimuli = get_lines_slide(10)
    for stim in stimuli:
        for ll in stim:
            print(ll)
        print("---")
        print(" ")

elif tests == 9:
    contact_types_tap = ['tap', 'tap-and-hold']
    n_iteration_per_stim = 10
    stim_list = []

    [points, lines] = get_tap_stimuli(n_iteration_per_stim)

    for t in contact_types_tap:
        for point in points:
            stim_list.append({
                'type': t,
                'size': 'point',
                'actuators': point,
                'direction': "None"
            })
        for line in lines:
            stim_list.append({
                'type': t,
                'size': 'line',
                'actuators': line,
                'direction': "None"
            })

    lines = get_points_slide(n_iteration_per_stim)
    matrices = get_lines_slide(n_iteration_per_stim)
    for line, direction in lines:
        stim_list.append({
            'type': "app-motion",
            'size': 'point',
            'actuators': line,
            'direction': direction
        })
    for matrix, direction in matrices:
        stim_list.append({
            'type': "app-motion",
            'size': 'line',
            'actuators': matrix,
            'direction': direction
        })

    for s in stim_list:
        print(s)
    print("------------------------------------------------------------")
    print(" ")
    random.shuffle(stim_list)
    for s in stim_list:
        print(s)

elif tests == 10:
    stim_list = get_stimuli(2)
    for s in stim_list:
        print(s)
    print("------------------------------------------------------------")
    print(" ")
    stim_list = random.sample(stim_list, len(stim_list))
    for s in stim_list:
        print(s)