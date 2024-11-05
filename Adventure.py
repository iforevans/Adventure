# Imports
import json 
 
# Constants - file names
FN_LOCATIONS = "locations.json"
FN_ITEMS = "items.json"

# Constants - item attributes
A_LIGHT = 1
A_HEAVY = 2
A_VERY_HEAVY = 3

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
L_CARRIED = "carried"
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

    def ToDict(self):
        # Convert the Location instance to a dictionary
        return {
            'name': self._name,
            'description': self._description,
            'exits': self._exits
        }

    # Set an exit from this location
    def SetExit(self, direction, name):
        self._exits[direction] = name

    # Get the description of the location
    def Describe(self):
        # print the location description
        print(f"\n{self._description}")
 
        # Any exits?
        if len(self._exits) > 0:
            print(f"Possible exits are:", end=" ")
            for key in self._exits:
                print(f" {key}", end= " ")

            #   Print a blank, seperator line
            print()
        else:
            print("Uh ho. There doesn't seem to be any way out of here!")

    # Get the location name
    def GetLocationName(self):
        return self._name

    # Move to a new location (if possible)
    def Move(self, direction):
        if direction.lower() in self._exits:
            return self._exits[direction]
        else:
            return None

class Item(object):
    def __init__(self):
        self._name = ""
        self._description = ""
        self._weight = 0
        self._location_name = ""
        self._requires_to_open = ""
        self._getable = False
        self._container = False
        self._open = False

    def ToDict(self):
        # Convert the item objects to a dictionary
        return {
            'name': self._name,
            'description': self._description,
            'weight': self._weight,
            'location_name' : self._location_name,
            'getable' : self._getable,
            'container' : self._container,
            'requires_to_open' : self._requires_to_open,
            'open' : self._open
        }

    # Some getters & setters
    def SetRequiresToOpen(self, requires_to_open):
        self._requires_to_open = requires_to_open

    def GetRequiresToOpen(self):
        return self._requires_to_open

    def SetDescription(self, description):
        self._description = description

    def GetDescription(self):
        # Are we a container?
        if self._container:
            # Yep, are we open?
            if self._open:
                # Yep, so describe as open
                return self._description + f" The {self._name} is open."
            else:
                # Nope, describe as closed
                return self._description + f" The {self._name} is closed."
        else:
            # Nope, not a container
            return self._description

    def SetOpen(self, open):
        self._open = open

    def GetOpen(self):
        return self._open

    def SetItemName(self, name):
        self._name = name

    def GetItemName(self):
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

    def SetLocationName(self, location):
        self._location_name = location

    def GetLocationName(self):
        return self._location_name


class Command(object):
    def __init__(self, verb, obj, prep, target):
        self._verb = verb
        self._obj = obj
        self._prep = prep
        self._target = target

    # Getters & Setters
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
            'with', 'at', 'from', 'onto',
            'using', 'into'
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
        # Initialize
        self._alive = True
        self._parser = Parser()
        self._items = {}
        self._map = {}

        # Create the game map & Items
        self.CreateMap()
        self.CreateItems()
        self._location = self._map[L_INSIDE_CABIN]

    def CreateItems(self):
        # Read the locations from the JSON file
        with open(FN_ITEMS, 'r') as json_file:
            items_list = json.load(json_file)

        # Create items from the loaded location dicts
        for item_dict in items_list:
            # Create the item object
            item = Item()

            # Populate it
            item.SetItemName(item_dict["name"])
            item.SetDescription(item_dict["description"])
            item.SetWeight(item_dict["weight"])
            item.SetLocationName(item_dict["location_name"])
            item.SetGetable(item_dict["getable"])
            item.SetContainer(item_dict["container"])
            item.SetRequiresToOpen(item_dict["requires_to_open"])
            item.SetOpen(item_dict["open"])

            # Add item
            self._items[item_dict["name"]] = item
            self._parser.AddObject(item_dict["name"])

    
    def CreateMap(self):
        # Read the locations from the JSON file
        with open(FN_LOCATIONS, 'r') as json_file:
            locations = json.load(json_file)

        # Create map from the loaded location dicts
        for location_dict in locations:
            # Create the location object
            location = Location(location_dict["name"], location_dict["description"])
            
            # Add any exits
            exit_dict = location_dict["exits"]
            if exit_dict is not None:
                for exit_name in exit_dict:
                    location.SetExit(exit_name, exit_dict[exit_name])
            
            # Add the location to the map
            self._map[location_dict["name"]] = location        

    # Move in a valid direction
    def Go(self, command):
        # Get the direction
        direction = command.GetObject()

        # Valid?
        if direction is not None:
            # Yep, try and move in that direction
            new_location_name = self._location.Move(direction)
            if new_location_name is not None:
                self._location = self._map[new_location_name]
            else:
                print(f"You can't go {direction}!")
        else:
            print("Sorry, I don't understand where you want to go...")

    # Get an item
    def Get(self, command):
        # Did we get a valid object name?
        if command.GetObject() is not None:
            # Yep, is it here?
            item = self._items[command.GetObject()]
            if item.GetLocationName() == self._location.GetLocationName():
                # Yep, present. Now, is it getable?
                if item.GetGetable():
                    item.SetLocationName(L_CARRIED)
                    print(f"You picked up the {item.GetItemName()}")
                else:
                    # Nope, not getable
                    print(f"You can't get the {item.GetItemName()}.")
            else:
                # Nope, not present
                print(f"I don't see a {item.GetItemName()} here!")
        else:
                print("Sorry, I don't understand what you want to get...")

    # Drop an item
    def Drop(self, command):
        # Do we have a valid object
        if command.GetObject() is not None:
            # Yep, so assume the object is an item name
            item = self._items[command.GetObject()]

            # Are we carrying it?
            if item.GetLocationName() == L_CARRIED:
                # Yep, so set the item's locstion to the current location
                item.SetLocationName(self._location.GetLocationName())
            else:
                # Nope, don't have it
                print(f"You are not carrying a {item.GetItemName()}!")
        else:
            # Nope
            print("Sorry, I don't understand what you want to drop...")

    # examine an item
    def Examine(self, command):
        # Did we get a valid object name?
        if command.GetObject() is not None:
            # Yep, is it here?
            item = self._items[command.GetObject()]
            if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                # Yep, print the longer description
                print(f"You examine the {item.GetItemName()}, and see: {item.GetDescription()}")
            else:
                # Nope, not here
                print(f"I don't see a {item.GetItemName()} anywhere!")
        else:
            # Nope,
            print("Sorry, I don't understand what you want to examine...")

    def GetCarriedItems(self):
        # Build list of all the items we are carrying
        carried = []
        for item_name in self._items:
            if self._items[item_name].GetLocationName() == L_CARRIED:
                carried.append(item_name)

        # Return the list
        return carried

    def Inventory(self):
        # Build list of all the items we are carrying
        carried = self.GetCarriedItems()

        # Tell the player what they are carrying
        if len(carried) > 0:
            print("You are carrying:", end=" ")
            for item_name in carried:
                print(f"{item_name}", end=" ")
        else:
            print("You are not carrying anything!")

    def OpenItem(self, item, command):
        target = command.GetTarget()
        obj = command.GetObject()

        # Do we have the item require to open?
        carried = self.GetCarriedItems()

        # Has the player tried to use the correct item to open?
        if target == item.GetRequiresToOpen():                
            if item.GetRequiresToOpen() in carried:
                # Yep, so open the item, and set all items within to now be in the current location
                for item_name in self._items:
                    if self._items[item_name].GetLocationName() == item.GetItemName():
                        # Set new item location to current location & mark as open
                        self._items[item_name].SetLocationName(self._location.GetLocationName())
                    
                # Mark item as open and update player
                self._items[obj].SetOpen(True) 
                print(f"You open the {obj}.")

            else:
                print(f"Sorry, you don't have what you need to open the {obj}.")
        else:
            print(f"You can't open the {item.GetItemName()} with that!")


    def Open(self, command):
        obj = command.GetObject()
        prep = command.GetPreposition()
        target = command.GetTarget()

        # Did we get a valid object name?
        if obj is not None:
            # Yep, valid prep?
            if prep == "with" or prep == "using":
                item = self._items[obj]
                if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                    # Is it a container?
                    if item.GetContainer():
                        self.OpenItem(item, command)
                    else:
                        # Nope, not a container
                        print(f"You can't open the {item.GetItemName()}!")
                else:
                    # Nope, not here
                    print(f"I don't see a {item.GetItemName()} anywhere!")
            else:
                print("Sorry, how do you want to open the chest?")
        else:
            # Nope,
            print("Sorry, I don't understand what you want to open...")

    def DoCommand(self, command):
        # Do this just once. DRY.
        verb = command.GetVerb()

        # What's our verb
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

    def DescribeLocation(self):
            # Describe the location
            self._location.Describe()

            # Show list of items here
            print("You can see the following items here:", end=" ")
            for item_name in self._items:
                item = self._items[item_name]
                if item.GetLocationName() == self._location.GetLocationName():
                    print(item_name, end=" ")
            print()


    # Main run method
    def Run(self):
        while (self._alive):
            # Tell the player where they are and what is there
            self.DescribeLocation()

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
