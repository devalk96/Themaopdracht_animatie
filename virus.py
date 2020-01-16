#!/usr/bin/env python3
"""
Createing objects for isualisation of the infection & replication 
of the Escherichia T4 Virus on the E.Coli bacteria.
"""

__author__ = "S. Bouwman, N. van der Linden"
__version__ = "1"

import math
import random
import copy
from pypovray import models
from vapory import Box, Cylinder, Torus, SphereSweep, Isosurface, \
    Function, ContainedBy, Texture, Pigment, Finish, Merge


def single_virus_gen():
    """
    single_virus_gen()
    Generates a virus object.
    :return virus object
    """
    object_texture = Texture(Pigment('color', [1, 1, 1], 'transmit', 0),
                             Finish('phong', 0.5, 'reflection', 0.9))

    helix_test = 'f_helix1(x, y, z, 1, 1 * 4 * pi, 0.07, 0.8, 1, 0.3, 0)'
    iso_spine = Isosurface(
        Function(helix_test),
        ContainedBy(Box(-5, 5)), 'translate', [0, 0, 0], models.default_sphere_model)  # spine helix

    cyl = Cylinder([0, -5, 0], [0, 5, 0], 0.5, object_texture)  # spine cylinder

    icosahedral = 'abs(x)+abs(y)+abs(z)-4.9'
    ico_head = Isosurface(
        Function(icosahedral),
        ContainedBy(Box(-3.5, 3.5)), 'max_gradient', 5,
        'translate', [0, 7, 0], object_texture)  # head object

    ring = Torus(1.2, 0.3, 'translate', [0, -5, 0], object_texture)  # hip ring spine

    # berelem radian, bijv: 1.05 * math.cos(radian * 3) 3 = step, 1.05 = straal
    radian = (360 / 6) * (math.pi / 180)

    x_tail_list = []
    for coordinate_offset in range(1, 7, 2):
        coordinate_offset += 0.05
        x_tail_list.append(coordinate_offset)  # [1.05, 3.05, 5.05]

    x_axis_tail_list = []
    z_axis_tail_list = []
    for tail_nr in range(1, 7):
        tail_steps = tail_nr
        for coordinate in x_tail_list:
            x_axis_tail_list.append(coordinate * math.cos(radian * tail_steps))
            z_axis_tail_list.append(coordinate * math.sin(radian * tail_steps))

    tails = []
    for tail_coordinate in range(0, len(x_axis_tail_list), 3):
        tails.append(SphereSweep('linear_spline', 3, [x_axis_tail_list[tail_coordinate], -5.00,
                                                      z_axis_tail_list[tail_coordinate]], 0.1,
                                 [x_axis_tail_list[tail_coordinate + 1], -1.00,
                                  z_axis_tail_list[tail_coordinate + 1]], 0.15,
                                 [x_axis_tail_list[tail_coordinate + 2], -9.00,
                                  z_axis_tail_list[tail_coordinate + 2]], 0.1, object_texture))
        # 6 tails

    virus_object = Merge(iso_spine, ico_head, ring, cyl)

    for tail in tails:
        virus_object.args.append(tail)

    return virus_object


def dna_gen(**kwargs):
    """
    dna_gen(size(int), -amount(int), -spacing(int))
    Generates a sphereweep of n amount of spheres. Following parameters are accepted:
    -xoffset(int), -y_offset(int), -z_offset(int), -texture(texture_object), -size(int), -amount(int), -spacing(int)

    mandatory:
    size(int), -amount(int), -spacing(int)

    If none is given default values are used:
    :return virus object
    """
    sphere_size = kwargs["size"]
    sphere_amount = kwargs["amount"]
    spacing = kwargs["spacing"]
    x_off = 0
    y_off = 0
    z_off = 0
    if "x_offset" in kwargs:
        x_off = kwargs["x_offset"]

    if "y_offset" in kwargs:
        y_off = kwargs["y_offset"]

    if "z_offset" in kwargs:
        z_off = kwargs["z_offset"]

    dna_string = SphereSweep('linear_spline', sphere_amount)
    for coordinate in range(sphere_amount):
        dna_string.args.append([x_off, +coordinate + -spacing + y_off, z_off])
        dna_string.args.append(sphere_size)

    if "texture" in kwargs:
        dna_string.args.append(kwargs["texture"])
    else:
        dna_string.args.append(models.default_sphere_model)

    return dna_string


def virus_multi_gen(**kwargs):
    """
    virus_multi_gen(**kwargs)
    Generates n amount of viruses. Following paramaters are accepted:
    -amount(int)

    If none is given default values is 10
    used.

    :return virus object
    """
    virus_count = 10
    if "amount" in kwargs:
        virus_count = kwargs["amount"]

    virus_obj = copy.deepcopy(single_virus_gen())
    virus_obj.args.append('translate')
    virus_obj.args.append([0, 0, 0])

    head = virus_obj.args[1]
    spine_object = Merge(virus_obj.args[1], virus_obj.args[3])
    tail_end_object = Merge(virus_obj.args[2])

    for number in range(4, 10):
        tail_end_object.args.append(virus_obj.args[number])

    head_copy = copy.deepcopy(head)
    head_copy.args.append('translate')
    head_copy.args.append([0, 0, 0])

    spine_copy = copy.deepcopy(spine_object)
    spine_copy.args.append('translate')
    spine_copy.args.append([0, 0, 0])

    tail_copy = copy.deepcopy(tail_end_object)
    tail_copy.args.append('translate')
    tail_copy.args.append([0, 0, 0])

    heads_list = []
    spines_list = []
    tails_list = []
    assemble_list = []
    explosion_list = []

    for i in range(virus_count):
        head_copy.args[8] = [random.randint(-80, 80), random.randint(-45, 45), random.randint(-25, 25)]
        spine_copy.args[3] = [random.randint(-80, 80), random.randint(-45, 45), random.randint(-25, 25)]
        tail_copy.args[8] = [random.randint(-75, 75), random.randint(-45, 45), random.randint(-24, 24)]
        assemble_coord = [random.randint(-75, 75), random.randint(-45, 45), random.randint(-22, 22)]
        explosion_coord = [random.randint(-600, 600), random.randint(-600, 600), random.randint(-600, 600)]

        new_head = copy.deepcopy(head_copy)
        new_spines = copy.deepcopy(spine_copy)
        new_tails = copy.deepcopy(tail_copy)

        heads_list.append(new_head)
        spines_list.append(new_spines)
        tails_list.append(new_tails)
        assemble_list.append(assemble_coord)
        explosion_list.append(explosion_coord)

    move_explosion = []
    for position in explosion_list:
        x_change = position[0] - assemble_list[explosion_list.index(position)][0]
        y_change = position[1] - assemble_list[explosion_list.index(position)][1]
        z_change = position[2] - assemble_list[explosion_list.index(position)][2]
        move_explosion.append([x_change, y_change, z_change])

    move_heads = []
    move_spines = []
    move_tails = []
    for position in assemble_list:
        x_change_heads = position[0] - heads_list[assemble_list.index(position)].args[8][0]
        y_change_heads = position[1] - heads_list[assemble_list.index(position)].args[8][1]
        z_change_heads = position[2] - heads_list[assemble_list.index(position)].args[8][2]

        x_change_spines = position[0] - spines_list[assemble_list.index(position)].args[3][0]
        y_change_spines = position[1] - spines_list[assemble_list.index(position)].args[3][1]
        z_change_spines = position[2] - spines_list[assemble_list.index(position)].args[3][2]

        x_change_tails = position[0] - tails_list[assemble_list.index(position)].args[8][0]
        y_change_tails = position[1] - tails_list[assemble_list.index(position)].args[8][1]
        z_change_tails = position[2] - tails_list[assemble_list.index(position)].args[8][2]

        move_heads.append([x_change_heads, y_change_heads, z_change_heads])
        move_spines.append([x_change_spines, y_change_spines, z_change_spines])
        move_tails.append([x_change_tails, y_change_tails, z_change_tails])

    return move_heads, move_spines, move_tails, move_explosion, heads_list, \
           spines_list, tails_list, assemble_list, explosion_list


if __name__ == '__main__':
    print(f"{single_virus_gen.__doc__} {'~' * 50}{virus_multi_gen.__doc__} {'~' * 50}{dna_gen.__doc__} {'~' * 50}")

