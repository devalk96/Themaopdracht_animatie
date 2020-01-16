#!/usr/bin/env python3
"""
Eindopdracht eindversie
Replication of bacteriophage Escherichia T4 virus. 
"""

__author__ = "N. van der Linden, S. Bouwman"
__version__ = "2019"

# Imports
import copy
import math
import virus
from pypovray import pypovray, SETTINGS, models, logger, load_config
from vapory import *

# Percentage of full scene
scene_1_percentage = 2
scene_2_percentage = 5
scene_3_percentage = 8

# filter of bacteria
inner_bacteria_filter = 0.9

# dna settings
dna_sphere_amount = 20
dna_spacing = 0.5

# init virus
move_heads, move_spines, move_tails, move_explosion, heads_list, spines_list, tails_list, \
assemble_list, explosion_list = virus.virus_multi_gen(amount=75)

heads_move = copy.deepcopy(move_heads)
spines_move = copy.deepcopy(move_spines)
tails_move = copy.deepcopy(move_tails)
explosion_move = copy.deepcopy(move_explosion)

heads = copy.deepcopy(heads_list)
spines = copy.deepcopy(spines_list)
tails = copy.deepcopy(tails_list)

assemble_pos = copy.deepcopy(assemble_list)
explosion_pos = copy.deepcopy(explosion_list)

explosion_pos_start = copy.deepcopy(assemble_pos)
heads_start = copy.deepcopy(heads_list)
spines_start = copy.deepcopy(spines_list)
tails_start = copy.deepcopy(tails_list)


# Define new classes
class Ring_Sphere(POVRayElement):
    """Function()"""


class Function(POVRayElement):
    """ Function()"""


class Icosahedron(POVRayElement):
    """ Function()"""


# Textures
virus_tail_spike_texture = Texture(Pigment('color', [0, 1, 0], 'filter', 0), Finish('phong', 1))

bacteria_texture_inner = Texture(Pigment('color', [0, 1, 0], 'transmit', 0),
                                 Finish('phong', 1, 'reflection', 0))
bacteria_texture_outer = Texture(Pigment('color', [0, 1, 0], 'transmit', 0.9),
                                 Finish('phong', 1, 'reflection', 0))


# Functions
def create_default_objects():
    """
    Creates the default objects used in each frame and returns them.
    """
    virus_single = createvirus_single()
    bacteria_inner, bacteria_outer = createbact()
    camera = Camera('location', [0, 50, -125], 'look_at', [0, 0, 0])
    camera_light = LightSource([0, 0, 0], 0.5)
    dna = virus.dna_gen(size=0.2, amount=dna_sphere_amount, y_offset=55, x_offset=0,
                        spacing=dna_spacing)
    return virus_single, bacteria_inner, bacteria_outer, camera, camera_light, dna


def createvirus_single():
    """
    Creates a single virus and sets default parameters
    :return virus object
    """
    to_add = ("translate", [0, 50, 5], "rotate", [0, 35, 0])
    new_virus = copy.deepcopy(virus.single_virus_gen())
    for object_modifier in to_add:
        new_virus.args.append(object_modifier)

    return new_virus


def createbact():
    """
    Creates a bacteria consisting of two individual spheresweeps. One large functioning as the
    outer membrane and one smaller functioning as the inner membrane.
    Both use a different texture.
    :return:
    """
    # type ('linear_spline', amount of spheres = 2, [x,y,z]_1, diameter_1, [x,y,z]_2, diameter_2,
    # texture.
    bacteria_inner = SphereSweep('linear_spline', 2, [-80, 0, 0], 55, [80, 0, 0], 55,
                                 bacteria_texture_inner)
    bacteria_outer = SphereSweep('linear_spline', 2, [-81, 0, 0], 57, [81, 0, 0], 57,
                                 bacteria_texture_outer)
    return bacteria_inner, bacteria_outer


def scene_1(step, scenepart, virus_single, bacteria_inner, bacteria_outer, camera):
    """
    0 - 20 %  of total frames
    First scene of render. This is the main scene 1 function. Starting other funcitons and
    returning the modified objects. This scene consists of the arrival and landing of the virus
    and makes up 20 percent of the total animation.
    """
    frames_in_scene = scenepart * 2
    virus_single, bacteria_inner = scene_1_virus(step, frames_in_scene, virus_single,
                                                 bacteria_inner)
    camera = scene_1_camera(virus_single, camera, frames_in_scene, step)
    return virus_single, bacteria_inner, bacteria_outer, camera


def scene_1_camera(virus_single, camera, frames_in_scene, step):
    """
    Handles the camera for scene 1. The camera needs to change throughout the scene. This
    function also needs various other parameters as they are needed to determine the location of
    the camera for the corresponding frame.
    :Return modified camera object modified corresponding to frames and virus coordinates
    """
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
        movement_per_frame_z = (zoom_out_distance - camera_distance) / (frames_per_part * 3)
        movement_per_frame_y = camera_distance / (frames_per_part * 3)

        new_virus_y = (current_virus_coord_y + camera_distance) - (
                (step - frames_per_part) * movement_per_frame_y)
        new_virus_z = (current_virus_coord_z + camera_distance) + (
                (step - frames_per_part) * movement_per_frame_z)
        camera.args[1] = [current_virus_coord_x, new_virus_y, new_virus_z]
        camera.args[3] = current_virus_coord

    return camera


def scene_1_virus(step, frames_in_scene, virus_single, bacteria_inner):
    """
    Handles the virus objects, as it needs to be modified throughout scene 1. This functions
    also requires various other parameters as they are needed to calculate the next position
    :Return modified virus and bacteria object corresponding to frame
    """
    # set constant values for virus particle
    virus_height = 10
    virus_standard_x = 10
    virus_standard_y = 55 + virus_height
    virus_standard_z = 0

    parts = 4
    frames_per_part = frames_in_scene / parts

    # part 1 consists of 2 * frames_per_part
    if step < (2 * frames_per_part):
        start_y = 250
        end_y = virus_standard_y

        # calculating step size to land on y_coordinate
        reach = start_y - end_y
        movement_per_frame = reach / (2 * frames_per_part)
        new_y = start_y - (step * movement_per_frame)

        virus_single.args[11] = [virus_standard_x, new_y, virus_standard_z]

    else:
        virus_single.args[11] = [virus_standard_x, virus_standard_y, virus_standard_z]

        filter_change = inner_bacteria_filter

        filter_change_per_step = filter_change / (frames_per_part * (parts / parts * 2))

        bacteria_inner.args[6].args[0].args[3] = (step - (
                2 * frames_per_part)) * filter_change_per_step

    return virus_single, bacteria_inner


def scene_2(step, scenepart, virus_single, bacteria_inner, bacteria_outer, camera, dna):
    """
    20 - 50 % of total frames
    Second scene of render. This is the main scene 2 function. Starting other functions and
    returning the modified objects. This scene consists of the injecting of the genetic material
    and makes up 30 percent of the total animation.
    """
    previous_frames = scenepart * scene_1_percentage
    bacteria_inner.args[6].args[0].args[3] = inner_bacteria_filter
    step = step - previous_frames
    frames_in_scene = scenepart * (scene_2_percentage - scene_1_percentage)
    virus_single = scene_2_virus(step, frames_in_scene, virus_single)
    dna = scene_2_dna(step, frames_in_scene, dna, virus_single)
    camera = scene_2_camera(virus_single, camera, frames_in_scene, step, dna)
    return virus_single, bacteria_inner, bacteria_outer, camera, dna


def scene_2_virus(step, frames_in_scene, virus_single):
    """
    Handles the virus objects, as it needs to be modified throughout scene 1. This functions
    also requires various other parameters as they are needed to calculate the next position
    :return modified virus object using the frames to calculate its position
    """
    # scene init
    parts = 4
    cylinder_length_increase = 1.5
    frames_per_part = frames_in_scene / parts

    # standard virus place
    virus_height = 10
    virus_standard_x = 10
    virus_standard_y = 55 + virus_height
    virus_standard_z = 0
    virus_single.args[11] = [virus_standard_x, virus_standard_y, virus_standard_z]

    # define max movement of head en cylinder comparing to virus
    total_movement_parts = -5

    if step < frames_per_part:
        # calculate movement per step
        movement_per_frame_y = total_movement_parts / frames_per_part

        # isosurface (head)
        virus_single.args[1].args[5][1] += movement_per_frame_y * step

        # cylinder
        virus_single.args[3].args[0][1] += (movement_per_frame_y * step) * cylinder_length_increase
        virus_single.args[3].args[1][1] += movement_per_frame_y * step

    elif (frames_per_part * 2) <= step < (frames_per_part * 3):
        step_corr = step - (frames_per_part * 2)

        movement_per_frame_y = (-total_movement_parts) / (
                (frames_per_part * 3) - (frames_per_part * 2))

        # isosurface (head)
        virus_single.args[1].args[5][1] += (movement_per_frame_y * step_corr) + total_movement_parts

        # cylinder
        virus_single.args[3].args[0][1] += ((movement_per_frame_y * step_corr) * (
                cylinder_length_increase - 1)) + total_movement_parts
        virus_single.args[3].args[1][1] += (movement_per_frame_y * step_corr) + total_movement_parts

    elif (frames_per_part * 3) <= step:  # Virus takeoff
        target_y = 125
        movement_per_frame_y = target_y / ((frames_per_part * 4) - (frames_per_part * 3))
        virus_single.args[11][1] += movement_per_frame_y * (step - (frames_per_part * 3))

    else:
        virus_single.args[1].args[5][1] += total_movement_parts
        virus_single.args[3].args[0][1] += total_movement_parts * cylinder_length_increase
        virus_single.args[3].args[1][1] += total_movement_parts

    return virus_single


def scene_2_camera(virus_single, camera, frames_in_scene, step, dna):
    """
    Handles the camera for scene 1. The camera needs to change throughout the scene. This
    function also needs various other parameters as they are needed to determine the location of
    the camera for the corresponding frame.
    :return modified camera object
    """
    parts = 4
    frames_per_part = frames_in_scene / parts
    camera_distance = 75
    camera.args[1] = [0, 0, -camera_distance]

    final_pos_z = -300

    movement_per_frame_z = (final_pos_z + camera_distance) / (
            (frames_per_part * 4) - (frames_per_part * 1.5))

    if (frames_per_part * 1.5) <= step < (frames_per_part * 2.5):
        camera.args[1][2] += movement_per_frame_z * (step - (frames_per_part * 1.5))
        camera.args[1][1] = dna.args[2][1] + 5
        if dna.args[2][1] <= 0:
            camera.args[3][1] = 0
        else:
            camera.args[3][1] = dna.args[2][1]

    elif (frames_per_part * 2.5) <= step:
        camera.args[1][2] += movement_per_frame_z * (step - (frames_per_part * 1.5))
        camera.args[1][1] = 0
        camera.args[3][1] = 0

    else:
        current_virus_coord = virus_single.args[11]
        current_virus_coord_x = current_virus_coord[0]
        current_virus_coord_y = current_virus_coord[1]
        current_virus_coord_z = current_virus_coord[2]
        camera.args[1] = [current_virus_coord_x, current_virus_coord_y,
                          current_virus_coord_z + camera_distance]
        camera.args[3] = current_virus_coord
    return camera


def scene_2_dna(step, frames_in_scene, dna, virus_single):
    """
    Handles the DNA/ genetic material which will be released by the virus. This function depends
    on various other parameters to calculate the coordinates for the DNA string. The DNA string
    is modeled with a sphere sweep and calculates the coordinates for each individual sphere in the
    sphere sweep
    :return modified dna objects
    """
    parts = 4
    frames_per_part = frames_in_scene / parts
    start_dna = 60

    dna_travel = -65
    movement_per_frame_y = dna_travel / ((frames_per_part * 2.5) - (frames_per_part * 1.5))

    # default dna location
    for coordinate in range(2, dna.args.__len__() - 1, 2):
        dna.args[coordinate] = [virus_single.args[11][0] - 1.7, start_dna, 0]

    if (frames_per_part * 1.5) <= step < (frames_per_part * 2.5):
        for coordinate in range(2, dna.args.__len__() - 1, 2):
            calc = movement_per_frame_y * (step - (frames_per_part * 1.5)) + (
                    coordinate * dna_spacing)
            if dna.args[coordinate][1] + calc < start_dna:
                dna.args[coordinate][1] += calc

            if dna.args[coordinate][1] + calc < 41:
                current_y = dna.args[coordinate][1] - start_dna
                x_coord = 1 * math.sin(current_y / 2) + 7
                dna.args[coordinate][0] = x_coord

    return dna


def scene_3(step, scenepart, bacteria_inner, bacteria_outer, camera):
    """
    50 - 80 % of total frames Third scene of render. This scene consists of the
    reproduction and assemblage of the virus particles and makes up 30 percent of the total
    animation.
    """

    previous_frames = scenepart * scene_2_percentage
    bacteria_inner.args[6].args[0].args[3] = inner_bacteria_filter
    step = step - previous_frames
    frames_in_scene = scenepart * (scene_3_percentage - scene_2_percentage)
    parts = frames_in_scene / 4
    fading_part = 2 * parts
    moving_part = 3 * parts

    fade_per_step = 1 / fading_part
    fade_start = 0

    if step <= fading_part:
        for head in heads:
            head.args[6].args[0].args[1][0] = fade_start + step * fade_per_step
            head.args[6].args[0].args[1][1] = fade_start + step * fade_per_step
            head.args[6].args[0].args[1][2] = fade_start + step * fade_per_step

        for spine in spines:
            spine.args[0].args[6].args[0].args[1][0] = fade_start + step * fade_per_step
            spine.args[0].args[6].args[0].args[1][1] = fade_start + step * fade_per_step
            spine.args[0].args[6].args[0].args[1][2] = fade_start + step * fade_per_step
            spine.args[1].args[3].args[0].args[1][0] = fade_start + step * fade_per_step
            spine.args[1].args[3].args[0].args[1][1] = fade_start + step * fade_per_step
            spine.args[1].args[3].args[0].args[1][2] = fade_start + step * fade_per_step

        for tail in tails:
            tail.args[0].args[4].args[0].args[1][0] = fade_start + step * fade_per_step

            for i in range(1, 7):
                tail.args[i].args[8].args[0].args[1][0] = fade_start + step * fade_per_step
                tail.args[i].args[8].args[0].args[1][1] = fade_start + step * fade_per_step
                tail.args[i].args[8].args[0].args[1][2] = fade_start + step * fade_per_step

    if step <= moving_part:
        for head in heads:
            head.args[8][0] = heads_start[heads.index(head)].args[8][0] + step * (
                    heads_move[heads.index(head)][0] / moving_part)
            head.args[8][1] = heads_start[heads.index(head)].args[8][1] + step * (
                    heads_move[heads.index(head)][1] / moving_part)
            head.args[8][2] = heads_start[heads.index(head)].args[8][2] + step * (
                    heads_move[heads.index(head)][2] / moving_part)

        for spine in spines:
            spine.args[3][0] = spines_start[spines.index(spine)].args[3][0] + step * (
                    spines_move[spines.index(spine)][0] / moving_part)
            spine.args[3][1] = spines_start[spines.index(spine)].args[3][1] + step * (
                    spines_move[spines.index(spine)][1] / moving_part)
            spine.args[3][2] = spines_start[spines.index(spine)].args[3][2] + step * (
                    spines_move[spines.index(spine)][2] / moving_part)

        for tail in tails:
            tail.args[8][0] = tails_start[tails.index(tail)].args[8][0] + step * (
                    tails_move[tails.index(tail)][0] / moving_part)
            tail.args[8][1] = tails_start[tails.index(tail)].args[8][1] + step * (
                    tails_move[tails.index(tail)][1] / moving_part)
            tail.args[8][2] = tails_start[tails.index(tail)].args[8][2] + step * (
                    tails_move[tails.index(tail)][2] / moving_part)

    elif moving_part < step:
        for head in heads:
            head.args[8] = assemble_pos[heads.index(head)]
        for spine in spines:
            spine.args[3] = assemble_pos[spines.index(spine)]
        for tail in tails:
            tail.args[8] = assemble_pos[tails.index(tail)]

    # Camera
    radian = (360 / 240) * (math.pi / 180)
    x_camera = 300 * math.cos(radian * (step + 180))
    z_camera = 300 * math.sin(radian * (step + 180))
    camera.args[1] = [x_camera, 0, z_camera]
    camera.args[3] = [0, 0, 0]

    return heads, spines, tails, bacteria_inner, bacteria_outer, camera


def scene_4(step, scenepart, bacteria_inner, bacteria_outer, camera):
    """
    80 - 100 %of total frames fourth scene of render. This scene consists of the
    reproduction and assemblage of the virus particles and makes up 30 percent of the total
    animation.
    """

    previous_frames = scenepart * scene_3_percentage
    bacteria_inner.args[6].args[0].args[3] = inner_bacteria_filter
    step = step - previous_frames
    frames_in_scene = scenepart * (10 - scene_3_percentage)

    for head in heads:
        head.args[8][0] = explosion_pos_start[heads.index(head)][0] + step * (
                explosion_move[heads.index(head)][0] / frames_in_scene)
        head.args[8][1] = explosion_pos_start[heads.index(head)][1] + step * (
                explosion_move[heads.index(head)][1] / frames_in_scene)
        head.args[8][2] = explosion_pos_start[heads.index(head)][2] + step * (
                explosion_move[heads.index(head)][2] / frames_in_scene)

    for spine in spines:
        spine.args[3][0] = explosion_pos_start[spines.index(spine)][0] + step * (
                explosion_move[spines.index(spine)][0] / frames_in_scene)
        spine.args[3][1] = explosion_pos_start[spines.index(spine)][1] + step * (
                explosion_move[spines.index(spine)][1] / frames_in_scene)
        spine.args[3][2] = explosion_pos_start[spines.index(spine)][2] + step * (
                explosion_move[spines.index(spine)][2] / frames_in_scene)

    for tail in tails:
        tail.args[8][0] = explosion_pos_start[tails.index(tail)][0] + step * (
                explosion_move[tails.index(tail)][0] / frames_in_scene)
        tail.args[8][1] = explosion_pos_start[tails.index(tail)][1] + step * (
                explosion_move[tails.index(tail)][1] / frames_in_scene)
        tail.args[8][2] = explosion_pos_start[tails.index(tail)][2] + step * (
                explosion_move[tails.index(tail)][2] / frames_in_scene)

    radian = (360 / 160) * (math.pi / 180)
    x_camera = 300 * math.cos(radian * (step + 120))
    z_camera = 300 * math.sin(radian * (step + 120))
    camera.args[1] = [x_camera, 0, z_camera]
    camera.args[3] = [0, 0, 0]

    return heads, spines, tails, bacteria_inner, bacteria_outer, camera


def scenehandle(step, scenepart, virus_single, bacteria_inner, bacteria_outer, camera, dna):
    """
    Handles all the individual scene functions, and determines which scene function should be
    called.
    :return Print to user providing information of current frame and current scene
    """
    sep = "."
    sep_dist = 25
    print("\n")

    if step <= (scenepart * scene_1_percentage):
        print(
            f"Current step: {step}".ljust(sep_dist, sep) + f"Scene 1 is till frame {scenepart * 2}")

        virus_single, bacteria_inner, bacteria_outer, camera = scene_1(step, scenepart,
                                                                       virus_single, bacteria_inner,
                                                                       bacteria_outer, camera)
        current_scene = 1

    elif (scenepart * scene_1_percentage) < step <= (scenepart * scene_2_percentage):
        print(f"Current step: {step}".ljust(sep_dist,
                                            sep) + f"Scene 2 is from frame {scenepart * 2} till "
                                                   f"{scenepart * 5}")

        virus_single, bacteria_inner, bacteria_outer, camera, dna = scene_2(step, scenepart,
                                                                            virus_single,
                                                                            bacteria_inner,
                                                                            bacteria_outer, camera,
                                                                            dna)
        current_scene = 2

    elif (scenepart * scene_2_percentage) < step <= (scenepart * scene_3_percentage):
        print(f"Current step: {step}".ljust(sep_dist,
                                            sep) + f"Scene 3 is from frame {scenepart * 5} till "
                                                   f"{scenepart * 8}")

        heads, spines, tails, bacteria_inner, bacteria_outer, camera = scene_3(step, scenepart,
                                                                               bacteria_inner,
                                                                               bacteria_outer,
                                                                               camera)
        current_scene = 3

    elif (scenepart * scene_3_percentage) <= step:
        print(f"Current step: {step}".ljust(sep_dist,
                                            sep) + f"Scene 4 is from frame {scenepart * 8} "
                                                   f"till {scenepart * 10}")

        heads, spines, tails, bacteria_inner, bacteria_outer, camera = scene_4(step, scenepart,
                                                                               bacteria_inner,
                                                                               bacteria_outer,
                                                                               camera)
        current_scene = 4

    return current_scene, virus_single, bacteria_inner, bacteria_outer, camera, dna


def frame(step):
    """
    Creates a new frame. Creates default objects by running create_default_objects() and sends
    these objects to scenehandle. Scenehandle returns these with the added information of which
    scene should be rendered corresponding to frame.
    :return objects needed to be rendered.
    """
    virus_single, bacteria_inner, bacteria_outer, camera_frame \
        , camera_light, dna = create_default_objects()
    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)
    scene_part = nframes * 0.1

    # Return the Scene object containing all objects for rendering
    current_scene, virus_single, bacteria_inner, bacteria_outer, camera_frame, dna = scenehandle(
        step, scene_part,
        virus_single,
        bacteria_inner,
        bacteria_outer,
        camera_frame, dna)
    # Light that will always follow the camera
    camera_light.args[0] = camera_frame.args[1]
    camera_light.args[0][2] += -15
    camera_light.args[1] = 0.1

    # main lighting
    main_light = models.default_light
    main_light.args[0] = [-15, 8, -40]

    # frame counter
    string = '"' + f"Frame nr: {str(step)}" + '"'
    frame_counter = Text('ttf', '"timrom.ttf"', '"s"', 1, 0, Pigment('color', [1, 1, 0]), "rotate",
                         [0, 180, 0],
                         "translate",
                         [camera_frame.args[1][0], camera_frame.args[1][1] + 5,
                          camera_frame.args[1][2] - 15])
    frame_counter.args[2] = string

    if current_scene == 1:  # rendering of scene 1
        return Scene(camera_frame,
                     objects=[main_light, virus_single, bacteria_inner, bacteria_outer,
                              camera_light],
                     included=["functions.inc", "shapes3.inc"])

    elif current_scene == 2:  # rendering of scene 2
        return Scene(camera_frame,
                     objects=[main_light, bacteria_outer, virus_single, dna, bacteria_inner],
                     included=["functions.inc", "shapes3.inc"])

    elif current_scene == 3:  # rendering of scene 3
        return Scene(camera_frame,
                     objects=[main_light, bacteria_inner, bacteria_outer] + heads + spines + tails,
                     included=["functions.inc", "shapes3.inc"])

    elif current_scene == 4:  # rendering of scene 4
        return Scene(camera_frame,
                     objects=[main_light, bacteria_inner, bacteria_outer] + heads + spines + tails,
                     included=["functions.inc", "shapes3.inc"])

    else:
        print(f"Error rendering frame {step}")


def main():
    """
    Main function performing the rendering Prints user information to sceen and grabs settings
    from settings file. Starts main render and creates .mp4 file
    """
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    pypovray.SETTINGS = load_config('default.ini')
    pypovray.render_scene_to_mp4(frame)
    return 0


if __name__ == '__main__':
    EXITCODE = main()
    exit(EXITCODE)
