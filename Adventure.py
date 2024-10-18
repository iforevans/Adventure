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
        # print the location description
        print(f"{self._description}")

        # Any items here?
        if len(self._items) > 0:
            print(f"You can see the following items here:", end=" ")
            for key in self._items:
                print(f" {self._items[key].ShortDescription()}")

        # Print any exits?
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

class Command(object):
    STATUS_VALID = "VALID"
    STATUS_INVALID = "INVALID"

    def __init__(self, command):
        # Define valid verbs & directions
        _valid_verbs = ["go", "get", "drop"]
        _valid_directions = ["north", "east", "south", "west", "in", "out", "up", "down"]

        # Split the user input into seperate words
        _words = command.split(' ')

        # We should get two words (verb-noun)
        if len(_words) == 2:
            # Do we have a valid verb?
            if _words[0] in _valid_verbs:
                _status = STATUS_VALID

        # If we get here, something was not good
        _status = STATUS_INVALID



            









