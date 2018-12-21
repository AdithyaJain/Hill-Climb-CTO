import math
import numpy as np
import random
from observer import *
from target import *
import copy
import time

env_height = 150
env_width = 150

# Variables
no_of_observers = 12
no_of_targets = 24

update_rate = 10
target_speed = 0.5

observer_sensor = 15
target_sensor = 15

size_of_subsets = 1
subsets = []
temp_list = []
for i in range(no_of_observers):
        temp_list.append(i)
        if i % size_of_subsets == size_of_subsets - 1:
            subsets.append(temp_list)
            temp_list = []
            continue
print(subsets)

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

    return np.array([destination_xx, destination_yy])
def no_of_targets_observed(observer, target):
    count = 0
    for targ in target:
        for obs in observer:
            if distance(targ.position, obs.position) <= observer_sensor:
                count += 1
                break
    return count
def check_H(observer, target):
    count = 0
    for obs in observer:
        for targ in target:
            if observer_sensor/2 < distance(obs.position, targ.position) < observer_sensor:
                count += distance(obs.position, targ.position)
    return count
def check_G(observer, target):
    observer_compliment = []
    for obs in observer:
        flag = 0
        for targ in target:
            if distance(obs.position, targ.position) <= observer_sensor:
                flag = 1
                break
        if flag == 0:
            observer_compliment.append(obs)
    target_compliment = []
    for targ in target:
        flag = 0
        for obs in observer:
            if distance(obs.position, targ.position) <= observer_sensor:
                flag = 1
                break
        if flag == 0:
            target_compliment.append(targ)

    count = 0
    for obs in observer_compliment:
        min = 200
        for targ in target_compliment:
            if min > distance(obs.position, targ.position):
                min = distance(obs.position, targ.position)
        count += min
    return count
def check_better(observer, observer_copy, target):
    if no_of_targets_observed(observer_copy, target) > no_of_targets_observed(observer, target):
        return True
    elif check_H(observer_copy, target) < check_H(observer, target):
        return True
    elif check_G(observer_copy, target) < check_G(observer, target):
        return True
    else:
        return False


result = 0
no_of_expts = 30

for exp in range(no_of_expts):
    start = time.time()

    observer = []
    for i in range(no_of_observers):
        observer.append(Observer(i, np.array([random.randint(0, env_width - 1), random.randint(0, env_height - 1)])))

    target = []
    for i in range(no_of_targets):
        target.append(Target(i, np.array([random.randint(0, env_width - 1), random.randint(0, env_height - 1)])))

    total_targets_observed = 0

    #############################
    # SIMULATION ################
    #############################
    for timestep in range(1500):
        # Update target list
        for obs in observer:
            obs.target_list = []
            for targ in target:
                if distance(obs.position, targ.position) <= observer_sensor:
                    obs.target_list.append(targ.tid)

        # COMPUTE OBSERVER'S DESTINATION
        if timestep % update_rate == 0:
            observer_destinations = [copy.deepcopy(i) for i in observer]
            for subset in subsets:
                box_height = env_height / 2
                box_width = env_width / 2
                for i in range(100):
                    observer_mutations = [copy.deepcopy(i) for i in observer_destinations]
                    to_mutate = random.choice(subset)
                    observer_mutations[to_mutate].position = random_destination(observer[to_mutate].position, box_height, box_width)
                    if box_height > env_height/10:
                        box_height = 0.99*box_height
                    if box_width > env_width/10:
                        box_width = 0.99*box_width

                    # Check if better
                    if check_better(observer_destinations, observer_mutations, target):
                        observer_destinations = observer_mutations
                # Update destinations
                for i in subset:
                    observer[i].destination = observer_destinations[i].position
                # for i in subset:
                #     min_dist = 200
                #     for j in subset:
                #         if min_dist > distance(observer[i].position, observer_destinations[j].position) and not (observer_destinations[j].position == np.array([-1, -1])).all():
                #             min_index = j
                #             min_dist = distance(observer[i].position, observer_destinations[j].position)
                #     observer[i].destination = observer_destinations[j].position
                #     observer_destinations[j].position = np.array([-1, -1])

        # COMPUTE TARGET'S DESTINATION
        for targ in target:
            if (targ.position == targ.destination).all():
                targ.destination = random_destination(targ.position, env_height/4, env_width/4)

        # COMPUTE NO OF TARGETS BEING OBSERVED IN TIME STEP
        no_of_targets_observed_per_time_step = no_of_targets_observed(observer, target)
        total_targets_observed += no_of_targets_observed_per_time_step

        # move towards destination
        for obs in observer:
            obs.move()
        for targ in target:
            targ.move(target_speed)

    avg_no_of_targets_observed_per_time_step = total_targets_observed / 1500
    result += avg_no_of_targets_observed_per_time_step
    print("Time taken for expt no " + str(exp) + " is: " + str(time.time() - start))
    print("Avg no of targets observed: " + str(avg_no_of_targets_observed_per_time_step))

print(result / no_of_expts)
