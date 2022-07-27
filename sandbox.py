#!/usr/bin/env python3

from include.actuators_info import *


points = get_random_edged_actuators(10)
# print(points)

directions = ("left", "up", "down", "right")
directions = random.sample(directions, len(directions))


tests = 3

if tests == 1:
    a_id_start = "p1"
    print(get_random_line(a_id_start, 2, directions))
elif tests == 2:
    sub_points = ["palm13", "palm23", "palm33"]
    lines = get_random_lines(sub_points)
    print(lines)
elif tests == 3:
    lines = get_random_lines(points)
    for l in lines:
        print(l)

