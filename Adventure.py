# This module will hold most of our classes

class Location(object):
    def __init__(self, loc_id, description):
        self._description = description
        self._loc_id = loc_id
        self._exits = {}
        self._items = {}

    # Set all the possible exits from this location
    def SetExits(self, N, E, S, W, I, O, U, D):
       self._exits = {"north":N, "east":E, "south":S, "west":W, "in":I, "out":O, "up":U, "down":D}

    # Get the description of the location
    def Describe(self):
        print(f"{self._description}")

        if len(self._items) > 0:
            print(f"You can see the following items here:", end=" ")
            for key in self._items:
                print(f" {self._items[key].ShortDescription()}")


        print(f"Possible exits are:", end=" ")
        for key in self._exits:
            if self._exits[key] != -1:
                print(f" {key}")

    # Move to a new location (if possible)
    def Move(self, direction):
        if direction.lower() in self._exits:
            return self._exits[direction]
        else:
            return -1

    # Drop an item at this location
    def DropItem(self, item):
        self._items[item.ItemId] = item

    # Get an item from this location
    def GetItem(self, item_id):
        if item_id in self._items:
            item = self._items(item_id)
            return item
    
class Item(object):
    def __init__(self, item_id, short_description, long_description, weight):
        self._item_id = item_id
        self._short_description = short_description
        self._long_description = long_description
        self._weight = weight

    def ItemId(self):
        return self._item_id

    def LongDescription(self):
        return self._long_description

    def ShortDescription(self):
        return self._short_description

    def Weight(self):
        return self._weight





