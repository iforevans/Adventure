# Imports
import json 
 
# Constants - file names
FN_LOCATIONS = "locations.json"
FN_ITEMS = "items.json"

# Constants - item attributes
A_LIGHT = 1
A_HEAVY = 2
A_VERY_HEAVY = 3

# Special Location
L_CARRIED = "carried"

# Constants - directions
D_NORTH = "north"
D_EAST = "east"
D_SOUTH = "south"
D_WEST = "west"
D_IN = "in"
D_OUT = "out"
D_UP = "up"
D_DOWN = "down"

class Location(object):
    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._start_location = False
        self._exits = {}
        self._blocked_exit = {}

    def ToDict(self):
        # Convert the Location instance to a dictionary
        return {
            'name': self._name,
            'description': self._description,
            'start_location' : self._start_location,
            'exits': self._exits,
            'blocked_exit': self._blocked_exit
        }

    # Getters & Setters
    def SetBlockedExit(self, blocked_exit):
        self._blocked_exit = blocked_exit

    def GetBlockedExit(self):
        return self._blocked_exit
    
    def AddExit(self, direction, name):
        self._exits[direction] = name

    # Get & Set Start Location 
    def GetStartLocation(self):
        return self._start_location
    
    def SetStartLocation(self, start_location):
        self._start_location = start_location

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
            # Doesn't look good for the player!
            print("Uh ho. There doesn't seem to be any way out of here!")
        
        # Is there a blocked exit?
        if len(self._blocked_exit) > 0:
            # Yep
            print(f"There is also {self._blocked_exit["desc"]}")
            
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
        self._getable = False
        self._container = False
        self._open = False
        self._locked = False
        self._requires_to_unlock = ""

    def ToDict(self):
        # Convert the item objects to a dictionary
        return {
            'name': self._name,
            'description': self._description,
            'weight': self._weight,
            'location_name' : self._location_name,
            'getable' : self._getable,
            'container' : self._container,
            'open' : self._open,
            'locked': self._locked,
            'requires_to_unlock' : self._requires_to_unlock
        }

    # Some getters & setters
    def SetLocked(self, locked):
        self._locked = locked

    def GetLocked(self):
        return self._locked

    def SetRequiresToUnlock(self, requires_to_unlock):
        self._requires_to_unlock = requires_to_unlock

    def GetRequiresToUnlock(self):
        return self._requires_to_unlock

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
            'unlock', 'lock', 'open', 'close', 'break',
            'smash', 'hit', 'help', 'quit'
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

        # These lists will hold valid names of things in our world
        self._item_names = []
        self._blocked_exit_names = []

    # Various checks
    def IsVerb(self, obj):
        if obj in self._verbs:
            return True
        return False

    def IsDirection(self, obj):
        if obj in self._directions:
            return True
        return False

    def IsItem(self, obj):
        if obj in self._item_names:
            return True
        return False

    def IsBlockedExit(self, obj):
        if obj in self._blocked_exit_names:
            return True
        return False

    # Add an known item
    def AddItemName(self, item_name):
        self._item_names.append(item_name)

    # Add a known blocked exit name
    def AddBlockedExitName(self, blocked_exit_name):
        self._blocked_exit_names.append(blocked_exit_name)

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
            elif not obj and (word in self._item_names or word in self._blocked_exit_names or word in self._directions):
                obj = word
            elif not prep and word in self._prepositions:
                prep = word
            elif prep and not target and (word in self._item_names or word in self._blocked_exit_names):
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
            item.SetOpen(item_dict["open"])
            item.SetLocked(item_dict["locked"])
            item.SetRequiresToUnlock(item_dict["requires_to_unlock"])

            # Add item
            self._items[item_dict["name"]] = item
            self._parser.AddItemName(item_dict["name"])

    
    def CreateMap(self):
        # Read the locations from the JSON file
        with open(FN_LOCATIONS, 'r') as json_file:
            locations_list = json.load(json_file)

        # Create map from the loaded location dicts
        for location_dict in locations_list:
            # Create the location object
            location = Location(location_dict["name"], location_dict["description"])
            
            # Get start_location flag
            location.SetStartLocation(location_dict["start_location"])

            # Any exits
            if "exits" in location_dict: 
                # Yep, so add it
                exits_dict = location_dict["exits"]
                for exit_name in exits_dict:
                    location.AddExit(exit_name, exits_dict[exit_name])

            # Is there a blocked exit for this location?
            if "blocked_exit" in location_dict:
                # Yep, add it
                blocked_exit_dict = location_dict["blocked_exit"]
                location.SetBlockedExit(blocked_exit_dict)
                self._parser.AddBlockedExitName(blocked_exit_dict["name"])

                
            # Check if this location is the start location
            if location.GetStartLocation():
                self._location = location

            # Add the location to the map
            self._map[location_dict["name"]] = location     

    # Move in a valid direction
    def Go(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Assume the object is the direction
        if obj is not None:
            # Yep, try and move in that direction
            new_location_name = self._location.Move(obj)
            if new_location_name is not None:
                self._location = self._map[new_location_name]
            else:
                print(f"You can't {verb} {obj}!")
        else:
            print(f"Sorry, I don't understand where you want to {verb}...")

    # Get an item
    def Get(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Did we get a valid object name?
        if obj is not None:
            # Yep, are we trying to get a valid item?
            if self._parser.IsItem(obj):
                item = self._items[obj]
                if item.GetLocationName() == self._location.GetLocationName():
                    # Yep, present. Now, is it getable?
                    if item.GetGetable():
                        item.SetLocationName(L_CARRIED)
                        print(f"You {verb} the {obj}")
                    else:
                        # Nope, not getable
                        print(f"You can't {verb} the {obj}...")
                else:
                    # Nope, not present
                    print(f"I don't see a {obj} here!")
            else:
                # Nope, not an item
                print(f"You can't {verb} the {obj}...")
        else:
                print(f"Sorry, I don't understand what you want to {verb}...")

    # Drop an item
    def Drop(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Do we have a valid object
        if obj is not None:
            # Yep, is it a valid item
            if obj in self._items:
                # Yep, 
                item = self._items[obj]

                # Are we carrying it?
                if item.GetLocationName() == L_CARRIED:
                    # Yep, so set the item's locstion to the current location
                    item.SetLocationName(self._location.GetLocationName())
                else:
                    # Nope, don't have it
                    print(f"You are not carrying a {item.GetItemName()}!")
            else:
                # Nope, not an item
                print(f"You can't {verb} the {obj}...")
        else:
            # Nope, no valid object specified
            print(f"Sorry, I don't understand what you want to {verb} ...")

    # Examine an item
    def Examine(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Did we get a valid object name?
        if obj is not None:
            # Yep, is it an item?
            if self._parser.IsItem(obj):
                # It's an item
                item = self._items[obj]
                if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                    # Yep, print the longer description
                    print(f"You {verb} the {obj}, and see: {item.GetDescription()}")
                else:
                    # Nope, not here
                    print(f"I don't see a {obj} anywhere!")
            # Is it a direction?
            elif self._parser.IsDirection(obj):
                # Yep. 
                print(f"You want to {verb} {obj}? Weird ...")
            else:
                print(f"You {verb} the {obj} but don't see anything more...")
        else:
            # Nope,
            print(f"Sorry, I don't understand what you want to {verb}...")

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

    def OpenItem(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Get a handle to the requested item
        item = self._items[obj]

        # Is the item here?
        if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
            # Is it a container?
            if item.GetContainer():
                # Is it locked?
                if not item.GetLocked():
                    inside = []
                    for item_name in self._items:
                        if self._items[item_name].GetLocationName() == item.GetItemName():
                            # Set new item location to current location & mark as open
                            self._items[item_name].SetLocationName(self._location.GetLocationName())
                            inside.append(item_name)
                
                    # Mark item as open and update player
                    self._items[obj].SetOpen(True) 
                    print(f"You {verb} the {obj}.")
            
                    # Tell player what was inside
                    print(f"Inside the {obj} you find: ", end=" ")
                    for item_name in inside:
                        print(f"{item_name}", end=" ")
                    print()
                else:
                    print(f"You can't {verb} the {obj}. It is locked.")
            else:
                # Nope, not a container
                print(f"You can't {verb} the {obj}!")
        else:
            # Nope, not here
            print(f"I don't see a {obj} anywhere!")

    def Open(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Did we get a valid object name?
        if obj is not None:
            # Yep. Is it an item?
            if obj in self._items:
                # Yep, deal with it.
                self.OpenItem(command)
            else:
                # Nope can't open that
                print(f"You can't {verb} the {obj}...")
        else:
            # Nope,
            print(f"Sorry, I don't understand what you want to {verb}...")

    def Close(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Did we get a valid object name?
        if obj is not None:
            # Yep, get the item
            item = self._items[obj]

            # Is the item present?
            if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                # Yep, is it a container?
                if item.GetContainer():
                    # Is it open?
                    if item.GetOpen():
                        item.SetOpen(False)
                        print(f"You {verb} the {obj}")
                    else:
                        print(f"The {obj} is already closed.")
                else:
                    # Nope, not a container
                    print(f"You can't {verb} the {obj}!")

            else:
                # Nope, not here
                print(f"I don't see a {obj} anywhere!")
        else:
            # Nope,
            print(f"Sorry, I don't understand what you want to {verb}...")

    def Lock(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Did we get a valid object name?
        if obj is not None:
            # Yep, get the item
            item = self._items[obj]

            # Is the item present?
            if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                # Yep, is it a container?
                if item.GetContainer():
                    # Is it open?
                    if not item.GetOpen():
                        item.SetLocked(True)
                        print(f"You {verb} the {obj}")
                    else:
                        # Nope
                        print(f"You can't {verb} the {obj} while it is open.")
                else:
                    # Nope, not a container
                    print(f"You can't {verb} the {obj}!")

            else:
                # Nope, not here
                print(f"I don't see a {obj} anywhere!")
        else:
            # Nope,
            print(f"Sorry, I don't understand what you want to {verb}...")

    def Unlock(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()
        prep = command.GetPreposition()
        target = command.GetTarget()

        # Did we get a valid object name?
        if obj is not None:
            if target is not None:
                # Yep, valid prep?
                if prep == "with" or prep == "using":
                    item = self._items[obj]

                    # Is the item here?
                    if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                        # Is it a container?
                        if item.GetContainer():
                            # Yep. Is it locked?
                            if item.GetLocked():
                                # Is the target item here?
                                target_item = self._items[target]
                                if target_item.GetLocationName() == self._location.GetLocationName() or target_item.GetLocationName() == L_CARRIED:
                                    # is the target the right item to unlock the item?
                                    if item.GetRequiresToUnlock() == target:
                                        # Yep, so unlock
                                        item.SetLocked(False)
                                        print(f"You {verb} the {obj}.")
                                    else:
                                        print(f"You can't {verb} the {obj} with the {target}")
                                else:
                                    # Nope, not here
                                    print(f"I don't see a {target} anywhere!")
                            else:
                                print(f"You can't {verb} the {obj}. It's already been done.")
                        else:
                            # Nope, not a container
                            print(f"You can't {verb} the {obj}!")
                    else:
                        # Nope, not here
                        print(f"I don't see a {obj} anywhere!")
                else:
                    print(f"Sorry, how do you want to {verb} the {obj}?")
            else:
                print(f"Sorry, I don't understand. What do you want to use to {verb} the {obj}?")
        else:
            # Nope,
            print(f"Sorry, I don't understand what you want to {verb}...")

    def HitItem(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()

        # Just do this for now
        print(f"You {verb} the {obj}. That was a waste of time, nothing happened.")
        
    def HitBlockedExit(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()
        prep = command.GetPreposition()
        target = command.GetTarget()

        # Is the exit the player is trying to hit even here?
        blocked_exit_dict = self._location.GetBlockedExit()
        if "name" in blocked_exit_dict and blocked_exit_dict["name"] == obj:
            # Yep, valid prep?
            if prep == "with" or prep == "using":
                # Is the player using the right item?
                if target == blocked_exit_dict["target"]:
                    # Yep. Add new exits
                    exits = blocked_exit_dict["exits"]
                    for direction in exits:
                        self._location.AddExit(direction, exits[direction])

                    # Update blocked exit description
                    blocked_exit_dict["desc"] = blocked_exit_dict["alt_desc"]

                    # Update player
                    effect = blocked_exit_dict["effect"]
                    print(f"You {verb} the {obj}. {effect}")
                else:
                    print(f"You {verb} the {obj}. It has no effect.")
            else:
                print(f"Sorry, how do you want to {verb} the {obj}?")
        else:
            print(f"I don't see a {obj} here for you to {verb}...")

    def Hit(self, command):
        verb = command.GetVerb()
        obj = command.GetObject()
        prep = command.GetPreposition()
        target = command.GetTarget()

        # Did we get a valid object name?
        if obj is not None:
            # Player is trying to hit an item?
            if self._parser.IsItem(obj):
                # Yep
                self.HitItem(command)
            # Player is trying to hit a blocked exit?
            elif self._parser.IsBlockedExit(obj):
                # Yep,
                self.HitBlockedExit(command)
            else:
                # Player must be trying to hit a direction
                print(f"You want to {verb} what? That makes no sense")
        else:
            # Nope,
            print(f"Sorry, I don't understand what you want to {verb}...")


    def DoCommand(self, command):
        # Do this just once. DRY.
        verb = command.GetVerb()

        # What's our verb
        # (Not using match/case here as it requires >= 3.10)
        if verb == "go":
            self.Go(command)
        if verb == 'hit' or verb == "break":
            self.Hit(command)
        elif verb == "get":
            self.Get(command)
        elif verb == "drop":
            self.Drop(command)
        elif verb == "open":
            self.Open(command)
        elif verb == "close":
            self.Close(command)
        elif verb == "lock":
            self.Lock(command)
        elif verb == "unlock":
            self.Unlock(command)
        elif verb == "examine":
            self.Examine(command)
        elif verb == "inventory":
            self.Inventory()

    def DescribeLocation(self):
            # Describe the location
            self._location.Describe()

            # Make a list of all the items that are in our current location
            here = []
            for item_name in self._items:
                item = self._items[item_name]
                if item.GetLocationName() == self._location.GetLocationName():
                    here.append(item_name)

            if len(here) > 0:
                # Show list of items here
                print("You can see the following items here:", end=" ")
                for item_name in here:
                    print(item_name, end=" ")
                print()
            else:
                print("There is nothing here.")

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
