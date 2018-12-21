import numpy as np


class Observer:
    def __init__(self, oid, position):
        self.oid = oid                      # Integer
        self.position = position            # 2 elt np array
        self.destination = position         # 2 elt np array
        self.target_list = []               # List of targets

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def move(self):
        position = self.position
        destination = self.destination
        if not (position == destination).all():
            direction_vector = destination - position
            magnitude = np.linalg.norm(direction_vector)
            unit_direction_vector = direction_vector / magnitude

            if magnitude < 1:
                self.position = destination
            else:
                self.position = position + unit_direction_vector
