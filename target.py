import numpy as np


class Target:
    def __init__(self, tid, position):
        self.tid = tid                          # Integer
        self.position = position                # 2 elt np array
        self.destination = position             # 2 elt np array
        self.obs_list = []                      # List of observers

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def move(self, speed):
        position = self.position
        destination = self.destination
        if position != destination:
            direction_vector = destination - position
            magnitude = np.linalg.norm(direction_vector)
            unit_direction_vector = direction_vector / magnitude

            if magnitude < speed:
                self.position = destination
            else:
                self.position = position + speed*unit_direction_vector

            # if self.position[0] < 0:
            #     self.position = (0, self.position[1])
            #     self.destination = self.position
            # if self.position[0] > 149:
            #     self.position = (149, self.position[1])
            #     self.destination = self.position
            #
            # if self.position[1] < 0:
            #     self.position = (self.position[0], 0)
            #     self.destination = self.position
            # if self.position[1] > 149:
            #     self.position = (self.position[0], 149)
            #     self.destination = self.position
