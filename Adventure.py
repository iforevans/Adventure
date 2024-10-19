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
        print(f"\n{self._description}")

        # Any items here?
        if len(self._items) > 0:
            print(f"You can see the following items here:", end=" ")
            for key in self._items:
                print(f" {self._items[key].Name()}", end=" ")

            #   Print a blank, seperator line
            print()
 

        # Print any exits?
        print(f"Possible exits are:", end=" ")
        for key in self._exits:
            if self._exits[key] != -1:
                print(f" {key}", end= " ")

        #   Print a blank, seperator line
        print()

    # Move to a new location (if possible)
    def Move(self, direction):
        if direction.lower() in self._exits:
            return self._exits[direction]
        else:
            return -1

    # Drop an item at this location
    def DropItem(self, item):
        self._items[item.Name()] = item

    # Get an item from this location
    def GetItem(self, item_name):
        # Is the item here?
        if item_name in self._items:
            # Yep, remove from the location and return it
            return self._items.pop(item_name)
        else:
            # Nope, not here
            return None
    
class Item(object):
    def __init__(self, name, description, weight):
        self._name = name
        self._description = description
        self._weight = weight

    def Description(self):
        return self._description

    def Name(self):
        return self._name

    def Weight(self):
        return self._weight

class Command(object):
    def __init__(self, command):
        # Default status of invalid
        self._valid = False

        # Define valid verbs & directions
        self._valid_verbs = ["go", "get", "drop", "examine", "quit"]
        self._valid_directions = ["north", "east", "south", "west", "in", "out", "up", "down"]

        # To hold our parsed command
        self._command = {}

        # Split the user input into seperate words
        self._words = command.split(' ')

        # We should get two words (verb-noun)
        if len(self._words) == 2:
            # Do we have a valid verb?
            if self._words[0] in self._valid_verbs:
                # Yep, save the nound and ver to our command dict
                self._command["verb"] = self._words[0]
                self._command["noun"] = self._words[1]
                self._valid = True
        elif len(self._words) == 1 and self._words[0] == "quit":
            # Valid quit command
            self._command["verb"] = self._words[0]
            self._command["noun"] = ""
            self._valid = True

    # Return our status
    def IsValid(self):
        return self._valid

    # Get the verb
    def GetVerb(self):
        if self._valid:
            return self._command["verb"]
        else:
            return None

    # Get the noun
    def GetNoun(self):
        if self._valid:
            return self._command["noun"]
        else:
            return None












