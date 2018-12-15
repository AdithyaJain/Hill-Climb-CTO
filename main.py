import math
import random
from observer import *
from target import *

env_height = 150
env_width = 150

# Variables
no_of_observers = 10
no_of_targets = 9

target_speed = 1.2

observer_sensor = 15
target_sensor = 15


def distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)


def random_destination(position):
    if position[0] < env_width/4:
        destination_xx = random.randint(0, math.floor(position[0] + env_width/4))
    elif position[0] + env_width/4 > env_width:
        destination_xx = random.randint(math.floor(position[0] - env_width/4), env_width-1)
    else:
        destination_xx = random.randint(math.floor(position[0] - env_width / 4), math.floor(position[0] + env_width/4))

    if position[1] < env_height/4:
        destination_yy = random.randint(0, math.floor(position[1] + env_height/4))
    elif position[1] + env_height/4 > env_height:
        destination_yy = random.randint(math.floor(position[1] - env_height/4), env_height-1)
    else:
        destination_yy = random.randint(math.floor(position[1] - env_height / 4), math.floor(position[1] + env_height/4))

    return destination_xx, destination_yy


result = 0
no_of_expts = 100

for exp in range(0, no_of_expts):
    observer = []
    for i in range(0, no_of_observers):
        observer.append(Observer(i, (random.randint(0, env_width - 1), random.randint(0, env_height - 1))))

    target = []
    for i in range(0, no_of_targets):
        target.append(Target(i, (random.randint(0, env_width - 1), random.randint(0, env_height - 1))))

    no_of_targets_observed_per_time_step = 0

    #############################
    # SIMULATION
    #############################
    for timestep in range(0, 1500):
        # COMPUTE OBSERVER'S DESTINATION
        if timestep % 10 == 0:
            for obs in observer:

                # Update target list
                obs.target_list = []
                for targ in target:
                    if distance(obs.get_position(), targ.get_position()) <= observer_sensor:
                        obs.target_list.append(targ.tid)  # TARGET LIST CONTAINS INDEX NUMBER OF TARGET

                # Compute destination
                # Random
                if not obs.target_list:
                    obs.set_destination(random_destination(obs.get_position()))
                # Mean position of targets
                else:
                    sum_target_position_x = sum_target_position_y = 0
                    length = len(obs.target_list)
                    for j in obs.target_list:
                        sum_target_position_x += target[j].get_position()[0]
                        sum_target_position_y += target[j].get_position()[1]
                    obs.set_destination((sum_target_position_x/length, sum_target_position_y/length))

        # COMPUTE TARGET'S DESTINATION
        for targ in target:
            if targ.get_position() == targ.get_destination():

                # Update observer list
                targ.obs_list = []
                for obs in observer:
                    if distance(obs.get_position(), targ.get_position()) <= target_sensor:
                        targ.obs_list.append(obs.oid)  # OBSERVER LIST CONTAINS INDEX NUMBER OF OBSERVER

                # Compute destination
                # Random
                if not targ.obs_list:
                    targ.set_destination(random_destination(targ.get_position()))
                # Mean position of observers
                else:
                    sum_obs_position_x = sum_obs_position_y = 0
                    length = len(targ.obs_list)
                    for j in targ.obs_list:
                        sum_obs_position_x += observer[j].get_position()[0]
                        sum_obs_position_y += observer[j].get_position()[1]
                    mean_obs = (sum_obs_position_x / length, sum_obs_position_y / length)
                    direction_vector = (targ.get_position()[0] - mean_obs[0], targ.get_position()[1] - mean_obs[1])
                    if direction_vector == (0, 0):
                        direction_vector = (random.randint(0, 1) - 0.5, random.randint(0, 1) - 0.5)
                    magnitude = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
                    unit_vector = (direction_vector[0] / magnitude, direction_vector[1] / magnitude)
                    destination_x = targ.get_position()[0] + 100 * unit_vector[0]
                    destination_y = targ.get_position()[1] + 100 * unit_vector[1]
                    targ.set_destination((destination_x, destination_y))

        # COMPUTE NO OF TARGETS BEING OBSERVED IN TIMESTEP
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
