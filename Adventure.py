# This module will hold most of our classes

class Game(object):
    def __init__(self):
        self._alive = True
        self._map = []
        self._location = None
        self._carried = {}

        # Create the game map & Items
        self.CreateMap()
        self.CreateItems()

        # Set starting location
        self._location = self._map[0]

    def CreateMap(self):
        # Create location 0
        location = Location(0, "You are inside a cabin in the woods.")
        location.SetExits(-1, -1, -1, -1, -1, 1, -1, -1)
        self._map.append(location)

        # Create location 1
        location = Location(1, "You are outside a small, wooden cabin in the woods. There is a tree here that looks climable!")
        location.SetExits(-1, -1, 2, -1, 0, -1, -1, -1)
        self._map.append(location)

        # Create location 2
        location = Location(2, "You are on a overgrown north/south path in the woods. The is what appears to be a deep, dark well here.")
        location.SetExits(1, -1, -1, -1, -1, -1, -1, 3)
        self._map.append(location)

        # Create location 3
        location = Location(3, "You are at the bottom of a very deep well. You can just see daylight overhead.")
        location.SetExits(-1, -1, -1, -1, -1, -1, 2, -1)
        self._map.append(location)

    def CreateItems(self):
        # Bottle
        item = Item("bottle", "The bottle is full of water", 1)
        self._map[0].DropItem(item)

        # Sword
        item = Item("sword", "A rusty old sword.", 3)
        self._map[1].DropItem(item)

    # Move in a valid direction
    def Move(self, direction):
        new_location_id = self._location.Move(direction)
        if new_location_id != -1:
            self._location = self._map[new_location_id]
        else:
            print(f"You can't go {direction}!")

    # Get an item
    def Get(self, item_name):
        # Get the Item
        item = self._location.GetItem(item_name)

        # Get it?
        if item is not None:
            # Yep, add it to carried dict
            self._carried[item.Name()] = item
            print(f"You picked up the {item.Name()}")
        else:
            # Nope
            print(f"I don't a {item_name} here!")

    # Drop an item
    def Drop(self, item_name):
        # Do we have the item
        if item_name in self._carried:
            # Yep, remove from carried and drop in current loc
            self._location.DropItem(self._carried.pop(item_name))
            print(f"You dropped the {item_name} here.")
        else:
            # Nope, don't have it
            print(f"You are not carrying the {item_name}!")

    # examine an item
    def Examine(self, item_name):
        # Do we have the item
        if item_name in self._carried:
            # Yep, print the longer derscription
            print(f"You examine the {item_name}, and see: {self._carried[item_name].Description()}")
        else:
            # Nope, don't have it
            print(f"You are not carrying the {item_name}, so you can't examine it!")

    def DoCommand(self, command):
        # Go command?
        if command.GetVerb() == "go":
            self.Move(command.GetNoun())
        elif command.GetVerb() == "get":
            self.Get(command.GetNoun())
        elif command.GetVerb() == "drop":
            self.Drop(command.GetNoun())
        elif command.GetVerb() == "examine":
            self.Examine(command.GetNoun())

    # Main run method
    def run(self):
        while (self._alive):
            # Tell the player where they are
            self._location.Describe()

            # What do they want to do?
            command = Command(input("What next? "))

            # Valid command
            if command.IsValid():
                if command.GetVerb() == "quit":
                    # We're done
                    print("You'll be back!")
                    self._alive = False
                else:
                    self.DoCommand(command)

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












