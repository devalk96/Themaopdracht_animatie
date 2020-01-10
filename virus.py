#!/usr/bin/env python3
"""
Visualisation of the infection & replication of the Escherichia T4 Virus on the E.Coli bacteria.
"""

__author__ = "S. Bouwman, N. van der Linden"
__version__ = "1"

from pypovray import models
from vapory import Box, Cylinder, Torus, SphereSweep, Isosurface, Function, ContainedBy, Texture, Pigment, Finish, Merge
import math


object_texture = Texture(Pigment('color', [1, 1, 1], 'filter', 0),
                             Finish('phong', 0.5, 'reflection', 0.9))

helix_test = 'f_helix1(x, y, z, 1, 1 * 4 * pi, 0.07, 0.8, 1, 0.3, 0)'
iso_test = Isosurface(
    Function(helix_test),
    ContainedBy(Box(-5, 5)), 'translate', [0,0,0], models.default_sphere_model) # spine helix

cyl = Cylinder([0, -5, 0], [0, 5, 0], 0.5, object_texture) # spine cylinder


icosahedral = 'abs(x)+abs(y)+abs(z)-4.9'
ico_test = Isosurface(
    Function(icosahedral),
    ContainedBy(Box(-3.5, 3.5)), 'max_gradient', 5, 'translate', [0, 7, 0], object_texture) # head object

ring = Torus( 1.2, 0.3, 'translate', [0, -5, 0], object_texture) # hip ring spine

radian = (360 / 6) * (math.pi / 180)  # bijv: 1.05 * math.cos(radian * 3)  3 = step, 1.05 = straal

x_tail_list = []
for x in range(1, 7, 2):
    x += 0.05
    x_tail_list.append(x) # [1.05, 3.05, 5.05]

x_axis_tail_list = []
z_axis_tail_list = []
for i in range(1, 7):
    tail_steps = i
    for x in x_tail_list:
        x_axis_tail_list.append(x * math.cos(radian * tail_steps))
        z_axis_tail_list.append(x * math.sin(radian * tail_steps))

tails = []
for f in range(0,len(x_axis_tail_list), 3):
    tails.append(SphereSweep('linear_spline', 3, [x_axis_tail_list[f], -5.00, z_axis_tail_list[f]], 0.1, [x_axis_tail_list[f + 1], -1.00, z_axis_tail_list[f + 1]], 0.15, [x_axis_tail_list[f + 2], -9.00, z_axis_tail_list[f + 2]], 0.1, object_texture))
    # 6 tails


virus_object = Merge(iso_test, ico_test, ring, cyl)

for tail in tails:
    virus_object.args.append(tail)

