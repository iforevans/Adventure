# Constants - directions
D_NORTH = "north"
D_EAST = "east"
D_SOUTH = "south"
D_WEST = "west"
D_IN = "in"
D_OUT = "out"
D_UP = "up"
D_DOWN = "down"

# Constants - location names
L_INSIDE_CABIN = "inside_cabin"
L_OUTSIDE_CABIN = "outside_cabin"
L_OVERGROWN_PATH = "overgrown_path"
L_BOTTOM_OF_WELL = "bottom_of_well"

class Game(object):
    def __init__(self):
        # Player attributes
        self._carried = {}
        self._alive = True

        # Game attributes
        self._map = {}
        self._location = None

        # Create the game map & Items
        self.CreateMap()
        self.CreateItems()

        # Set starting location
        self._location = self._map[0]

    def CreateMap(self):
        # Create Locations. Eventually we will get all this from a map file
        location = Location(L_INSIDE_CABIN, "You are inside a cabin in the woods.")
        location.SetExit(D_OUT, L_OUTSIDE_CABIN)
        self._map[location.Name] = location

        # Outside cabin
        location = Location(L_OUTSIDE_CABIN, "You are outside a small, wooden cabin in the woods. There is a tree here that looks climable!")
        location.SetExit(D_IN, L_INSIDE_CABIN)
        location.SetExit(D_SOUTH, L_OVERGROWN_PATH)
        self._map[location.Name] = location

        # Overgrown path
        location = Location(L_OVERGROWN_PATH, "You are on a overgrown north/south path in the woods. The is what appears to be a deep, dark well here.")
        location.SetExit(D_DOWN, L_BOTTOM_OF_WELL)
        location.SetExit(D_NORTH, L_OUTSIDE_CABIN)
        self._map[location.Name] = location

        # Bottom of well
        location = Location(L_BOTTOM_OF_WELL, "You are at the bottom of a very deep, but now dry well. You can just see daylight overhead.")
        location.SetExit(D_UP, L_OVERGROWN_PATH)
        self._map[location.Name] = location

    def CreateItems(self):
        # Bottle
        item = Item("bottle", "The bottle is full of water", 1)
        self._map[L_INSIDE_CABIN].DropItem(item)

        # Sword
        item = Item("sword", "A rusty old sword.", 3)
        self._map[L_BOTTOM_OF_WELL].DropItem(item)

    # Move in a valid direction
    def Go(self, direction):
        new_location = self._location.Move(direction)
        if new_location is not None:
            self._location = self._map[new_location]
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

    def Inventory(self):
        # List all the items we are carrying
        if len(self._carried) > 0:
            print("You are carrying: ", end=" ")
            for item_name in self._carried:
                print(f"{item_name} ")
        else:
            print("You are not carrying anything!")

    def DoCommand(self, command):
        # Go command?
        if command.GetVerb() == "go":
            self.Go(command.GetNoun())
        elif command.GetVerb() == "get":
            self.Get(command.GetNoun())
        elif command.GetVerb() == "drop":
            self.Drop(command.GetNoun())
        elif command.GetVerb() == "examine":
            self.Examine(command.GetNoun())
        elif command.GetVerb() == "inventory":
            self.Inventory()

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
    def __init__(self,name, description):
        self._name = name
        self._description = description
        self._exits = {}
        self._items = {}

    # Set an exit from this location
    def SetExit(self, direction, name):
        self._exits[direction] = name

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
 
        # Any exits?
        if len(self._exits) > 0:
            print(f"Possible exits are:", end=" ")
            for key in self._exits:
                if self._exits[key] != -1:
                    print(f" {key}", end= " ")

            #   Print a blank, seperator line
            print()
        else:
            print("Uh ho. There doesn't seem to be any way out of here!")

    # Get the location name
    def Name(self):
        return self._name

    # Move to a new location (if possible)
    def Move(self, direction):
        if direction.lower() in self._exits:
            return self._exits[direction]
        else:
            return None

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
        self._valid_verbs = ["go", "get", "drop", "examine", "inventory", "quit"]
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
        elif len(self._words) == 1 and self._words[0] == "inventory":
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
