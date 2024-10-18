# This module will hold most of our classes

class Location(object):

    def __init__(self, loc_id, description):
        self._description = description
        self._loc_id = loc_id

    def SetExits(self, N, E, S, W, I, O, U, D):
       self._exits = {"north":N, "east":E, "south":S, "west":W, "in":I, "out":O, "up":U, "down":D}

    def Describe(self):
        print(f"{self._description}")
        print(f"Possible exits are:", end=" ")
        for key in self._exits:
            if self._exits[key] != -1:
                print(f" {key}")

    def Move(self, direction):
        if direction.lower() in self._exits:
            return self._exits[direction]
        else:
            return -1


class Item(object):
    def __init__(self, item_id, short_description, long_description, weight):
        self._item_id = item_id
        self._short_description = short_description
        self._long_description = long_description
        self._weight = weight


