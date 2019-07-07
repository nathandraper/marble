from collections import defaultdict
import json
import math
import random
# all methods assume the use of a defaultdict when reading the level data

# Constructor signatures for objects:
# Bullet: def __init__(self, location, texture, rows_cols, velocity, angle):
# Block:  def __init__(self, location, texture, rows_cols, width, height, velocity):

FPS = 30
DEFAULT_BULLET_SPRITE = "bullet_texture.png"
DEFAULT_BLOCK_SPRITE = "skull_block.png"
DEFAULT_ROWS_COLS = (2, 5)
DEFAULT_VELOCITY = 5

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 800


def special_dict():
    return defaultdict(lambda: defaultdict(list))


def load_json_to_special_dict(jason):
    # a special defaultdict matching the level data format. The default value of the outer dictionary (with the frame as
    # a key) is an empty defaultdict with a default of an empty list (for object parameters)
    with open(jason) as f:
        result = json.load(f, object_hook=lambda x: defaultdict(lambda: defaultdict(list), x))
    return result


def time_to_frames(string):
    mins, secs = string.split(":")
    return (60 * int(mins) + int(secs)) * FPS


def merge_wave(level_dic, *args):
    for dic in args:
        for frame, obj_dic in dic.items():
            for obj_name, obj_list in obj_dic.items():
                level_dic[frame][obj_name].extend(obj_list)


def set_win_time(level_dic, time):
    frame = time_to_frames(time)
    level_dic[frame] = "win"


def set_level_drag(level_dic, drag):
    level_dic["drag"] = drag


def set_map(level_dic):
    level_dic["map"] = {"platform": [], "platform_enabled": 0}


def shoot_bullet(time, location, angle, velocity=DEFAULT_VELOCITY,
                 rows_cols=DEFAULT_ROWS_COLS, texture=DEFAULT_BULLET_SPRITE):
    time = time_to_frames(time)
    wave = special_dict()
    bullet = [location, texture, rows_cols, velocity, angle]
    wave[time]["bullets"].append(bullet)
    return wave


def rain_bullets(time, density, angle=(3*math.pi)/2, velocity=DEFAULT_VELOCITY, pulses=1, pulse_shift=0, interval=FPS,
                 cascading=False, origin="top", texture=DEFAULT_BULLET_SPRITE, rows_cols=DEFAULT_ROWS_COLS):
    # Create a rain of bullets at time "time". By default, bullets come from the top of the screen straight down (angle)
    # The number of bullets in the rain is equal to "density"
    # The rain can repeat a number of times specified by "pulses"
    # The time between pulses is "interval"
    # The x_pos of the bullets can alternate each pulse by an amount of pixels equal to "pulse_shift"
    # if cascading is True, the bullets in each pulse will spawn at even sub-intervals depending on the density
    # TODO implement origin to spawn bullets from different sides of the screen
    switch = False
    wave = special_dict()
    time = time_to_frames(time)
    for pulse in range(pulses):
        cascade_interval = math.floor(interval/density) if cascading else 0
        for x in range(density):
            frame = time + (pulse*interval) + (cascade_interval*x)
            x_pos = (SCREEN_WIDTH/density)*x + (SCREEN_WIDTH/(density*2)) + pulse_shift*switch
            bullet = [[math.floor(x_pos), 0], texture, rows_cols, velocity, angle]
            wave[frame]["bullets"].append(bullet)
            switch = not switch

    return wave


def death_spiral(time, density, velocity=DEFAULT_VELOCITY, pulses=1, interval=FPS, cascading=False, origin=(0, 0),
                 texture=DEFAULT_BULLET_SPRITE, rows_cols=DEFAULT_ROWS_COLS):
    # TODO fix this mess
    wave = special_dict()
    time = time_to_frames(time)

    perimeter = SCREEN_HEIGHT*2 + SCREEN_WIDTH*2
    space = perimeter/density
    x_pos, y_pos = origin
    spaces = 0

    for pulse in range(pulses):
        cascade_interval = math.floor(interval/density) if cascading else 0
        for x in range(density):
            try:
                angle = math.atan2((y_pos - SCREEN_HEIGHT / 2), -(x_pos - SCREEN_WIDTH / 2))
            except ZeroDivisionError:
                angle = math.copysign(math.pi/2, -y_pos + SCREEN_HEIGHT / 2)

            frame = time + (pulse*interval) + (cascade_interval*x)
            bullet = [[math.floor(x_pos), math.floor(y_pos)], texture, rows_cols, velocity, angle]
            wave[frame]["bullets"].append(bullet)

            # determine x and y positions based on sections of the perimeter
            spaces += space
            if spaces < SCREEN_WIDTH:
                x_pos += space
            elif SCREEN_WIDTH < spaces < SCREEN_WIDTH + SCREEN_HEIGHT:
                y_pos += space
            elif SCREEN_WIDTH + SCREEN_HEIGHT < spaces < SCREEN_WIDTH * 2 + SCREEN_HEIGHT:
                x_pos -= space
            elif SCREEN_WIDTH * 2 + SCREEN_HEIGHT < spaces:
                y_pos -= space

        return wave

# Bullet: def __init__(self, location, texture, rows_cols, velocity, angle):
def radiate(time, density, arc, velocity=DEFAULT_VELOCITY, pulses=1, interval=FPS, cascading=False,
            origin=(SCREEN_WIDTH/2, 0), texture=DEFAULT_BULLET_SPRITE, rows_cols=DEFAULT_ROWS_COLS):
    wave = special_dict()
    start_frame = time_to_frames(time)
    cut = arc/density
    x = origin[0] - SCREEN_WIDTH/2
    y = -(origin[1] - SCREEN_HEIGHT/2)

    try:
        angle_to_center = math.atan2(-y, -x)
    except ZeroDivisionError:
        angle_to_center = math.copysign(math.pi / 2, y)

    angles = [angle_to_center - (arc/2) + (cut/2) + (cut*bullet)  for bullet in range(density)]

    for pulse in range(pulses):
        cascade_interval = math.floor(interval/density) if cascading else 0
        for x in range(density):
            frame = start_frame + cascade_interval*x + interval*pulse
            bullet = [origin, texture, rows_cols, velocity, angles[x]]
            wave[frame]["bullets"].append(bullet)
    return wave




if __name__ == "__main__":
    #a = rain_bullets("0:03", 7, pulses=3, interval=FPS*3)
    #b = death_spiral("0:12", 15, pulses=2, interval=FPS*3)
    a = radiate("0:5", 4, math.pi/2, pulses=3, origin=(100,100), cascading=True)
    c = radiate("0:10", 7, math.pi/2, pulses=3)
    b = death_spiral("0:15", 15, pulses=2, interval=FPS*2)
    d = rain_bullets("0:20", 7, pulses=3, interval=FPS*3)
    merge_wave(a, b, c, d)
    set_level_drag(a, 3)
    set_map(a)
    set_win_time(a, "0:25")

    with open("level_2", "w") as f:
        json.dump(a, f, indent=2)
