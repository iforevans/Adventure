# Constants - item attributes
A_LIGHT = 1
A_HEAVY = 2
A_VERY_HEAVY = 3
A_OPEN = "open"
A_CLOSED = "closed"

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
L_TOP_OF_TREE = "top_of_tree"
L_OVERGROWN_PATH = "overgrown_path"
L_BOTTOM_OF_WELL = "bottom_of_well"

class Location(object):
    def __init__(self, name, description):
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
                print(f" {self._items[key].GetName()}", end=" ")

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
        self._items[item.GetName()] = item

    def IsPresent(self, item_name):
        # Is the item here?
        if item_name in self._items:
            # Yep, it is
            return True

        # Nope, not here
        return False

    def IsGetable(self, item_name):
        # First, is it even here?
        if item_name in self._items:
            # Yep, now, is it getable?
            return self._items[item_name].GetGetable()

        # Nope, 
        return False

    # Get an item from this location
    def GetItem(self, item_name):
        # Remove the item from this location and return
        return self._items.pop(item_name)

class Item(object):
    def __init__(self):
        self._name = ""
        self._description = ""
        self._weight = 0
        self._getable = False
        self._container = False
        self._items = {}
        self._requiresToOpen = ""
        self._status = A_CLOSED

    # Some getters & setters
    def SetDescription(self, description):
        self._description = description

    def GetDescription(self):
        return self._description

    def SetName(self, name):
        self._name = name

    def GetName(self):
        return self._name

    def SetWeight(self, weight):
        self._weight = weight

    def GetWeight(self):
        return self._weight

    def SetContainer(self, container):
        self._container = container

    def GetContainer(self):
        return self._container

    def SetGetable(self, getable):
        self._getable = getable

    def GetGetable(self):
        return self._getable

    # Class Methods
    def TakeFrom(self, name):
        # Item inside?
        if name in self._items:
            # Yep, removed from container items and return
            return self._items.pop(name)
        else:
            # Nope, not here
            return None

    def PutIn(self, item):
        # Valid item?
        if item is not None:
            self._items[item.GetName()] = item


class Command(object):
    def __init__(self, verb, obj, prep, target):
        self._verb = verb
        self._obj = obj
        self._prep = prep
        self._target = target

    def GetVerb(self):
        return self._verb

    def GetObject(self):
        return self._obj

    def GetPreposition(self):
        return self._prep

    def GetTarget(self):
        return self._target

class Parser(object):
    def __init__(self):
        # Valid verbs
        self._verbs = [
            'go', 'get', 'drop', 'examine', 'inventory',
            'examine', 'open', 'close', 'attack', 'inventory',
            'put', 'take', 'help', 'quit'
        ]
        
        # Valid directions
        self._directions = [
            'north', 'east', 'south', 'west',
            'in', 'out', 'up', 'down'
        ]

        #  Valid preps
        self._prepositions = [
            'at', 'on', 'in', 'with', 'to', 'from', 'into', 'onto',
            'through', 'over', 'under', 'behind', 'toward'
        ]

        # This should be added to as objects are created
        self._objects = []

    # Add an object to our objects list
    def AddObject(self, object_name):
        self._objects.append(object_name)

    # Parse the user input
    def ParseInput(self, user_input):
        verb = None
        obj = None
        prep = None
        target = None

        # Break user input into tokens
        tokens = user_input.lower().split()

        # Parse the tokens
        for word in tokens:
            if not verb and word in self._verbs:
                verb = word
            elif not obj and (word in self._objects or word in self._directions):
                obj = word
            elif not prep and word in self._prepositions:
                prep = word
            elif prep and not target and (word in self._objects or word in self._directions):
                target = word

        # Return parsed user input as a command object
        return Command(verb, obj, prep, target)

# This is the main game object!
class Game(object):
    def __init__(self):
        # Player attributes
        self._carried = {}
        self._alive = True

        # Game attributes
        self._parser = Parser()
        self._map = {}
        self._location = None

        # Create the game map & Items
        self.CreateMap()

        # Set starting location
        self._location = self._map[L_INSIDE_CABIN]

    def CreateMap(self):
        # Create Locations. Eventually we will get all this from a map file

        # Create location
        location = Location(L_INSIDE_CABIN, "You are inside a cabin in the woods.")
        location.SetExit(D_OUT, L_OUTSIDE_CABIN)

        # Create bottle
        item = Item()
        item.SetName("bottle")
        item.SetDescription("The bottle is full of water")
        item.SetWeight(A_LIGHT)
        item.SetGetable(True)
        item.SetContainer(False)
        self._parser.AddObject("bottle")
        location.DropItem(item)
        self._map[location.Name()] = location

        # Create location
        location = Location(L_OUTSIDE_CABIN, "You are outside a small, wooden cabin in the woods. There is a tree here that looks climable!")
        location.SetExit(D_IN, L_INSIDE_CABIN)
        location.SetExit(D_UP, L_TOP_OF_TREE)
        location.SetExit(D_SOUTH, L_OVERGROWN_PATH)
        self._map[location.Name()] = location

        # Create location
        location = Location(L_TOP_OF_TREE, "You are at the very top of a tall tree. The branches are very thin here.")
        location.SetExit(D_DOWN, L_OUTSIDE_CABIN)

        # Create key
        item = Item()
        item.SetName("key")
        item.SetDescription("A small golden key.")
        item.SetWeight(A_LIGHT)
        item.SetGetable(True)
        item.SetContainer(False)
        self._parser.AddObject("key")
        location.DropItem(item)
        self._map[location.Name()] = location

        # Create location
        location = Location(L_OVERGROWN_PATH, "You are on a overgrown north/south path in the woods. The is what appears to be a deep, dark well here.")
        location.SetExit(D_DOWN, L_BOTTOM_OF_WELL)
        location.SetExit(D_NORTH, L_OUTSIDE_CABIN)
        self._map[location.Name()] = location

        # Create location
        location = Location(L_BOTTOM_OF_WELL, "You are at the bottom of a very deep, but now dry well. You can just see daylight high overhead.")
        location.SetExit(D_UP, L_OVERGROWN_PATH)

        # Create chest
        chest = Item()
        chest.SetName("chest")
        chest.SetDescription("A very strong, heavy chest. The chest is locked and too heavy to move.")
        chest.SetWeight(A_VERY_HEAVY)
        chest.SetGetable(False)
        chest.SetContainer(True)
        self._parser.AddObject("chest")

        # Create sword
        sword = Item()
        sword.SetName("sword")
        sword.SetDescription("A rusty old sword. It still looks dangerous, though!")
        sword.SetWeight(A_HEAVY)
        sword.SetGetable(True)
        sword.SetContainer(False)
        self._parser.AddObject("sword")

        # Put the sword in the chest
        chest.PutIn(sword)
        location.DropItem(chest)
        self._map[location.Name()] = location

    # Move in a valid direction
    def Go(self, command):
        # Get the direction
        direction = command.GetObject()

        # Valid?
        if command.GetObject() is not None:
            # Yep, try and move in that direction
            new_location = self._location.Move(direction)
            if new_location is not None:
                self._location = self._map[new_location]
            else:
                print(f"You can't go {direction}!")
        else:
            print("Sorry, I don't understand where you want to go...")

    # Get an item
    def Get(self, command):
        # Did we get a valid object?
        if command.GetObject() is not None:
            # Yep, so assume the object is an item name and try and get it
            item_name = command.GetObject()
            if self._location.IsPresent(item_name):
                # Yep, present. Now, is it getable?
                if self._location.IsGetable(item_name):
                    # Yep, present and getable
                    self._carried[item_name] = self._location.GetItem(item_name)
                    print(f"You picked up the {item_name}")
                else:
                    # Nope, not getable
                    print(f"You can't get the {item_name}.")
            else:
                # Nope, not present
                print(f"I don't see a {item_name} here!")
        else:
                print("Sorry, I don't understand what you want to get...")


    # Drop an item
    def Drop(self, command):
        # Do we have a valid object
        if command.GetObject() is not None:
            # Yep, so assume the object is an item name
            item_name = command.GetObject()

            # Are we carrying it?
            if item_name in self._carried:
                # Yep, remove from carried and drop in current loc
                self._location.DropItem(self._carried.pop(item_name))
                print(f"You dropped the {item_name} here.")
            else:
                # Nope, don't have it
                print(f"You are not carrying a {item_name}!")
        else:
            # Nope
            print("Sorry, I don't understand what you want to drop...")

    # examine an item
    def Examine(self, command):
        # Do we have a valid object?
        if command.GetObject() is not None:
            # Yep, assume the object is the item name
            item_name = command.GetObject()

            # Are we carrying it?
            if item_name in self._carried:
                # Yep, print the longer derscription
                print(f"You examine the {item_name}, and see: {self._carried[item_name].GetDescription()}")
            elif item_name in self._location._items:
                # Item is here
                print(f"You examine the {item_name}, and see: {self._location._items[item_name].GetDescription()}")
            else:
                # Nope, don't have it
                print(f"I don't see a {item_name}, anywhere!")
        else:
            # Nope,
            print("Sorry, I don't understand what you want to examine...")

    def Inventory(self):
        # List all the items we are carrying
        if len(self._carried) > 0:
            print("You are carrying:", end=" ")
            for item_name in self._carried:
                print(f"{item_name}", end=" ")
        else:
            print("You are not carrying anything!")

    def Open(self, command):
        # Do we have a valid object
        if command.GetObject() is not None:
            # Yep, so assume the object is an item name
            item_name = command.GetObject()

            if self._location.IsPresent(item_name):
                pass
        else:
            # Nope
            print("Sorry, I don't understand what you want to open...")


    def DoCommand(self, command):
        # Do this just once. DRY.
        verb = command.GetVerb()

        # What's our verb?
        # (Not using match/case here as it requires >= 3.10)
        if verb == "go":
            self.Go(command)
        elif verb == "get":
            self.Get(command)
        elif verb == "drop":
            self.Drop(command)
        elif verb == "open": 
            self.Open(command)
        elif verb == "examine":
            self.Examine(command)
        elif verb == "inventory":
            self.Inventory()

    # Main run method
    def run(self):
        while (self._alive):
            # Tell the player where they are
            self._location.Describe()

            # What do they want to do?
            command = self._parser.ParseInput(input("What next? "))

            # Valid command
            if command.GetVerb() == None:
                print("Sorry, I don't understand what you said ...")
            elif command.GetVerb() == "quit":
                print("You'll be back!")
                self._alive = False
            else:
                self.DoCommand(command)

