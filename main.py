import math
import numpy as np
import random
from observer import *
from target import *

env_height = 150
env_width = 150

# Variables
no_of_observers = 12
no_of_targets = 24

target_speed = 0.5

observer_sensor = 15
target_sensor = 15


def distance(coord1, coord2):
    return np.linalg.norm(coord1 - coord2)


def random_destination(position, height, width):
    if position[0] < width/2:
        destination_xx = random.randint(0, math.floor(position[0] + width/2))
    elif position[0] + width/2 > env_width:
        destination_xx = random.randint(math.floor(position[0] - width/2), env_width-1)
    else:
        destination_xx = random.randint(math.floor(position[0] - width/2), math.floor(position[0] + width/2))

    if position[1] < height/2:
        destination_yy = random.randint(0, math.floor(position[1] + height/2))
    elif position[1] + height/2 > env_height:
        destination_yy = random.randint(math.floor(position[1] - height/2), env_height-1)
    else:
        destination_yy = random.randint(math.floor(position[1] - height/2), math.floor(position[1] + height/2))

    return destination_xx, destination_yy


result = 0
no_of_expts = 100

for exp in range(no_of_expts):
    observer = []
    for i in range(no_of_observers):
        observer.append(Observer(i, (random.randint(0, env_width - 1), random.randint(0, env_height - 1))))

    target = []
    for i in range(no_of_targets):
        target.append(Target(i, (random.randint(0, env_width - 1), random.randint(0, env_height - 1))))

    no_of_targets_observed_per_time_step = 0

    #############################
    # SIMULATION
    #############################
    for timestep in range(0, 1500):
        # COMPUTE OBSERVER'S DESTINATION
                # Update target list
                # Compute destination

        # COMPUTE TARGET'S DESTINATION
                # Update observer list
                # Compute destination

        # COMPUTE NO OF TARGETS BEING OBSERVED IN TIME STEP
        for targ in target:
            if targ.obs_list:
                no_of_targets_observed_per_time_step += 1

        # move towards destination
        for obs in observer:
            obs.move()
        for targ in target:
            targ.move(target_speed)

    avg_no_of_targets_observed_per_time_step = no_of_targets_observed_per_time_step / 1500
    result += avg_no_of_targets_observed_per_time_step

print(result / no_of_expts)
