#!/usr/bin/env python3
"""Eindopdracht eindversie"""

__author__ = "N. van der Linden, S. Bouwman"
__version__ = "2019"

# Imports
import sys
from pypovray import pypovray, SETTINGS, models, logger, load_config
from vapory import *
import math
import copy
import virus


inner_bacteria_filter = 0

# Define new classes
class Ring_Sphere(POVRayElement):
    """Function()"""


class Function(POVRayElement):
    """ Function()"""


class Icosahedron(POVRayElement):
    """ Function()"""


# Constants


# Textures
virus_tail_spike_texture = Texture(Pigment('color', [0, 1, 0], 'filter', 0), Finish('phong', 1))

bacteria_texture_inner = Texture(Pigment('color', [0, 1, 0], 'filter', 0), Finish('phong', 1, 'reflection', 0))
bacteria_texture_outer = Texture(Pigment('color', [0, 1, 0], 'filter', 0.9), Finish('phong', 1, 'reflection', 0))


# Functions
def create_default_objects():
    virus_single = createvirus_single()
    virus_list = createvirus_multi()
    bacteria_inner, bacteria_outer = createbact()
    camera = Camera('location', [0, 50, -125], 'look_at', [0, 0, 0])
    return virus_single, virus_list, bacteria_inner, bacteria_outer, camera


def createvirus_single():
    to_add = ("translate", [0, 50, 5], "rotate", [0, 35, 0])
    new_virus = copy.deepcopy(virus.virus_object)
    for object_modifier in to_add:
        new_virus.args.append(object_modifier)

    return new_virus


def createvirus_multi():
    virus_list = []
    for i in range(10):
        new_virus = copy.deepcopy(virus.virus_object)
        virus_list.append(new_virus)
    return virus_list


def createbact():
    # type ('linear_spline', amount of spheres = 2, [x,y,z]_1, diameter_1, [x,y,z]_2, diameter_2, texture.
    bacteria_inner = SphereSweep('linear_spline', 2, [-80, 0, 0], 55, [80, 0, 0], 55, bacteria_texture_inner)
    bacteria_outer = SphereSweep('linear_spline', 2, [-82, 0, 0], 59, [82, 0, 0], 59, bacteria_texture_outer)
    return bacteria_inner, bacteria_outer


def scene_1(step, scenepart, virus_single, bacteria_inner, bacteria_outer, camera):
    """0 - 20 %"""
    frames_in_scene = scenepart * 2
    virus_single = scene_1_virus(step, frames_in_scene, virus_single)
    camera = scene_1_camera(virus_single, camera, frames_in_scene, step)
    return virus_single, bacteria_inner, bacteria_outer, camera


def scene_1_camera(virus_single, camera, frames_in_scene, step):
    parts = 4
    camera_distance = 35
    zoom_out_distance = 75

    frames_per_part = frames_in_scene / parts

    current_virus_coord = virus_single.args[11]
    current_virus_coord_x = current_virus_coord[0]
    current_virus_coord_y = current_virus_coord[1]
    current_virus_coord_z = current_virus_coord[2]

    # part1 camera
    if step < frames_per_part:
        camera.args[1] = [current_virus_coord_x, current_virus_coord_y + camera_distance,
                          current_virus_coord_z + camera_distance]
        camera.args[3] = current_virus_coord

    if step >= frames_per_part:
        print(f"Current frame = {step - frames_per_part}")

        movement_per_frame_z = (zoom_out_distance - camera_distance) / (frames_per_part * 3)
        movement_per_frame_y = camera_distance / (frames_per_part * 3)
        print(
            f"in {frames_per_part * 3} the Z should change to {zoom_out_distance}. \t Z per frame {movement_per_frame_z}")

        new_virus_y = (current_virus_coord_y + camera_distance) - ((step - frames_per_part) * movement_per_frame_y)
        new_virus_z = (current_virus_coord_z + camera_distance) + ((step - frames_per_part) * movement_per_frame_z)
        camera.args[1] = [current_virus_coord_x, new_virus_y, new_virus_z]
        camera.args[3] = current_virus_coord

    return camera


def scene_1_virus(step, frames_in_scene, virus_single):
    # set constant values for virus particle
    virus_height = 10
    virus_standard_x = 10
    virus_standard_y = 55 + virus_height
    virus_standard_z = 0

    parts = 4
    frames_per_part = frames_in_scene / parts
    print("Allocated frames per part in scene 1: ", frames_per_part)

    # part 1 consists of 2 * frames_per_part
    if step < (2 * frames_per_part):
        start_y = 250
        end_y = virus_standard_y

        # calculating step size to land on y_coordinate
        reach = start_y - end_y
        movement_per_frame = reach / (2 * frames_per_part)
        new_y = start_y - (step * movement_per_frame)

        print(f"New Y coordinate for frame {step} is {round(new_y, 2)}")
        virus_single.args[11] = [virus_standard_x, new_y, virus_standard_z]

    else:
        virus_single.args[11] = [virus_standard_x, virus_standard_y, virus_standard_z]

    return virus_single


def scene_2(step, scenepart, virus_list, bacteria_inner, bacteria_outer, camera):
    """20 - 50 %"""
    return virus_list, bacteria_inner, bacteria_outer, camera


def scene_3(step, scenepart, virus_list, bacteria_inner, bacteria_outer, camera):
    """50 - 80 %"""
    return virus_list, bacteria_inner, bacteria_outer, camera


def scene_4(step, scenepart, virus_list, bacteria_inner, bacteria_outer, camera):
    """80 - 100 %"""
    return virus_list, bacteria_inner, bacteria_outer, camera


def scenehandle(step, scenepart, virus_single, virus_list, bacteria_inner, bacteria_outer, camera):
    sep = "."
    sep_dist = 25
    print("\n")
    if step <= (scenepart * 2):
        print(f"Current step: {step}".ljust(sep_dist, sep) + f"Scene 1 is till frame {scenepart * 2}")
        virus_single, bacteria_inner, bacteria_outer, camera = scene_1(step, scenepart, virus_single, bacteria_inner,
                                                                       bacteria_outer, camera)
        current_scene = 1

    elif (scenepart * 2) < step <= (scenepart * 5):
        print(f"Current step: {step}".ljust(sep_dist,
                                            sep) + f"Scene 2 is from frame {scenepart * 2} till {scenepart * 5}")
        virus_list, bacteria_inner, bacteria_outer, camera = scene_2(step, scenepart, virus_list, bacteria_inner,
                                                                     bacteria_outer, camera)
        current_scene = 2

    elif (scenepart * 5) < step <= (scenepart * 8):
        print(f"Current step: {step}".ljust(sep_dist,
                                            sep) + f"Scene 3 is from frame {scenepart * 5} till {scenepart * 8}")
        virus_list, bacteria_inner, bacteria_outer, camera = scene_3(step, scenepart, virus_list, bacteria_inner,
                                                                     bacteria_outer, camera)
        current_scene = 3

    elif step > (scenepart * 8):
        print(f"Current step: {step}".ljust(sep_dist,
                                            sep) + f"Scene 4 is from frame {scenepart * 8} till {scenepart * 10}")
        virus_list, bacteria_inner, bacteria_outer, camera = scene_4(step, scenepart, virus_list, bacteria_inner,
                                                                     bacteria_outer, camera)
        current_scene = 4

    return current_scene, virus_single, virus_list, bacteria_inner, bacteria_outer, camera


def frame(step):
    virus_single, virus_list, bacteria_inner, bacteria_outer, camera_frame = create_default_objects()
    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)
    scene_part = nframes * 0.1
    # Return the Scene object containing all objects for rendering
    current_scene, virus_single, virus_list, bacteria_inner, bacteria_outer, camera_frame = scenehandle(step,
                                                                                                        scene_part,
                                                                                                        virus_single,
                                                                                                        virus_list,
                                                                                                        bacteria_inner,
                                                                                                        bacteria_outer,
                                                                                                        camera_frame)

    if current_scene == 1:  # rendering of scene 1
        return Scene(camera_frame,
                     objects=[models.default_light, virus_single, bacteria_inner, bacteria_outer],
                     included=["functions.inc", "shapes3.inc"])

    elif current_scene == 2:  # rendering of scene 2
        return Scene(camera_frame,
                     objects=[models.default_light, bacteria_inner, bacteria_outer] + virus_list,
                     included=["functions.inc", "shapes3.inc"])

    elif current_scene == 3:  # rendering of scene 3
        return Scene(camera_frame,
                     objects=[models.default_light, bacteria_inner, bacteria_outer] + virus_list,
                     included=["functions.inc", "shapes3.inc"])

    elif current_scene == 4:  # rendering of scene 4
        return Scene(camera_frame,
                     objects=[models.default_light, bacteria_inner, bacteria_outer] + virus_list,
                     included=["functions.inc", "shapes3.inc"])

    else:
        print(f"Error rendering frame {step}")


def main():
    """ Main function performing the rendering """
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    pypovray.SETTINGS = load_config('default.ini')
    pypovray.render_scene_to_mp4(frame, range(241))

    return 0


if __name__ == '__main__':
    EXITCODE = main()
    exit(EXITCODE)
