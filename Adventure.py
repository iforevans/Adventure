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
 
        # Is there a blocked exit?
        if len(self._blocked_exit) > 0:
            # Yep
            print(f"There is {self._blocked_exit["desc"]}")
        
        # Any normal exits?
        if len(self._exits) > 0:
            # Yep, so list exits
            print(f"Possible exits are:", end=" ")
            for key in self._exits:
                print(f" {key}", end= " ")
            print()
        else:
            # No exits. Doesn't look good for the player!
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
        self.verb = verb
        self.obj = obj
        self.prep = prep
        self.target = target

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
            'with', 'at',
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
            # Found a verb?
            if not verb and word in self._verbs:
                verb = word
            # Found object (of the sentance)?
            elif not obj and (word in self._item_names or word in self._blocked_exit_names or word in self._directions):
                obj = word
            # Found a preposition?
            elif not prep and word in self._prepositions:
                prep = word
            # Found the target?
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
        # Assume the object is the direction
        if command.obj is not None:
            # Yep, try and move in that direction
            new_location_name = self._location.Move(command.obj)
            if new_location_name is not None:
                self._location = self._map[new_location_name]
            else:
                # Not a valid direction
                print(f"You can't {command.verb} {command.obj}!")
        else:
            # No obj specified
            print(f"Sorry, I don't understand where you want to {command.verb}...")

    # Get an item
    def Get(self, command):
        # Did we get a valid object name?
        if command.obj is not None:
            # Yep, are we trying to get a valid item?
            if self._parser.IsItem(command.obj):
                item = self._items[command.obj]
                if item.GetLocationName() == self._location.GetLocationName():
                    # Yep, present. Now, is it getable?
                    if item.GetGetable():
                        item.SetLocationName(L_CARRIED)
                        print(f"You {command.verb} the {command.obj}")
                    else:
                        # Item not gettable
                        print(f"You can't {command.verb} the {command.obj}...")
                else:
                    # Item not present
                    print(f"I don't see the {command.obj} here!")
            else:
                # Not an item
                print(f"You can't {command.verb} the {command.obj}...")
        else:
            # No valid obj
            print(f"Sorry, I don't understand what you want to {command.verb}...")

    # Drop an item
    def Drop(self, command):
        # Do we have a valid object
        if command.obj is not None:
            # Yep, is it a valid item?
            if command.obj in self._items:
                # Yep, 
                item = self._items[command.obj]

                # Are we carrying it?
                if item.GetLocationName() == L_CARRIED:
                    # Yep, so set the item's locstion to the current location
                    item.SetLocationName(self._location.GetLocationName())
                else:
                    # Item not carried
                    print(f"You are not carrying the {command.obj}!")
            else:
                # Not a valid item
                print(f"You can't {command.verb} the {command.obj}...")
        else:
            # No valid obj
            print(f"Sorry, I don't understand what you want to {command.verb} ...")

    # Examine an item
    def Examine(self, command):
        # Did we get a valid object name?
        if command.obj is not None:
            # Yep, is it an item?
            if self._parser.IsItem(command.obj):
                # It's an item
                item = self._items[command.obj]
                if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                    # Yep, print the longer description
                    print(f"You {command.verb} the {command.obj}, and see: {item.GetDescription()}")
                else:
                    # Nope, not here
                    print(f"I don't see a {command.obj} anywhere!")
            # Is it a direction?
            elif self._parser.IsDirection(command.obj):
                # Yep, strange request, but you never know
                print(f"You want to {command.verb} {command.obj}? Weird ...")
            else:
                # Fallback feedback
                print(f"You {command.verb} the {command.obj} but don't see extra details...")
        else:
            # No valid obj
            print(f"Sorry, I don't understand what you want to {command.verb}...")

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
        # Get a handle to the requested item
        item = self._items[command.obj]

        # Is the item here?
        if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
            # Is it a container?
            if item.GetContainer():
                # Is it locked?
                if not item.GetLocked():
                    # Nope, Get all the stuff out
                    inside = []
                    for item_name in self._items:
                        if self._items[item_name].GetLocationName() == item.GetItemName():
                            # Set new item location to current location & mark as open
                            self._items[item_name].SetLocationName(self._location.GetLocationName())
                            inside.append(item_name)
                
                    # Mark item as open and update player
                    self._items[command.obj].SetOpen(True) 
                    print(f"You {command.verb} the {command.obj}.")
            
                    # Tell player what was inside
                    print(f"Inside the {command.obj} you find: ", end=" ")
                    for item_name in inside:
                        print(f"{item_name}", end=" ")
                    print()
                else:
                    # Item already locked
                    print(f"You can't {command.verb} the {command.obj}. It is locked.")
            else:
                # Item not a container
                print(f"You can't {command.verb} the {command.obj}!")
        else:
            # Item not here
            print(f"I don't see a {command.obj} anywhere!")

    def Open(self, command):
        # Did we get a valid object name?
        if command.obj is not None:
            # Yep. Is it an item?
            if self._parser.IsItem(command.obj):
                # Yep, deal with it.
                self.OpenItem(command)
            else:
                # Nope can't open that
                print(f"You can't {command.verb} the {command.obj}...")
        else:
            # Nope,
            print(f"Sorry, I don't understand what you want to {command.verb}...")

    def Close(self, command):
        # Did we get a valid object name?
        if command.obj is not None:
            # Yep, now, is it an item?
            if self._parser.IsItem(command.obj):
                # Yep, get the item
                item = self._items[command.obj]

                # Is the item present?
                if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                    # Yep, is it a container?
                    if item.GetContainer():
                        # Is it open?
                        if item.GetOpen():
                            item.SetOpen(False)
                            print(f"You {command.verb} the {command.obj}")
                        else:
                            # Closed already
                            print(f"The {command.obj} is already closed.")
                    else:
                        # Not a container
                        print(f"You can't {command.verb} the {command.obj}!")
                else:
                    # Not here
                    print(f"I don't see a {command.obj} anywhere!")
            else:
                # Not an item
                print(f"You can't {command.verb} a {command.obj}")
        else:
            # Unknown object,
            print(f"Sorry, I don't understand what you want to {command.verb}...")

    def Lock(self, command):
        # Did we get a valid object name?
        if command.obj is not None:
            # Yep, get the item
            item = self._items[command.obj]

            # Is the item present?
            if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                # Yep, is it a container?
                if item.GetContainer():
                    # Is it open?
                    if not item.GetOpen():
                        # Is the target item here?
                        target_item = self._items[command.target]
                        if target_item.GetLocationName() == self._location.GetLocationName() or target_item.GetLocationName() == L_CARRIED:
                            # is the target the right item to unlock the item?
                            if item.GetRequiresToUnlock() == command.target:
                                # Yep. Lock!
                                item.SetLocked(True)
                                print(f"You {command.verb} the {command.obj}")
                            else:
                                print(f"You can't {command.verb} the {command.obj} with the {command.target}")
                        else:
                            # Target not here
                            print(f"I don't see a {command.target} here ...")
                    else:
                        # Can't lock while open
                        print(f"You can't {command.verb} the {command.obj} while it is open.")
                else:
                    # Not a container
                    print(f"You can't {command.verb} the {command.obj}!")
            else:
                # Item not here
                print(f"I don't see a {command.obj} anywhere!")
        else:
            # No valid object
            print(f"Sorry, I don't understand what you want to {command.verb}...")

    def Unlock(self, command):
        # Did we get a valid object name?
        if command.obj is not None:
            # Valid target?
            if command.target is not None:
                # Yep, valid prep?
                if command.prep == "with" or command.prep == "using":
                    item = self._items[command.obj]

                    # Is the item here?
                    if item.GetLocationName() == self._location.GetLocationName() or item.GetLocationName() == L_CARRIED:
                        # Is it a container?
                        if item.GetContainer():
                            # Yep. Is it locked?
                            if item.GetLocked():
                                # Is the target item here?
                                target_item = self._items[command.target]
                                if target_item.GetLocationName() == self._location.GetLocationName() or target_item.GetLocationName() == L_CARRIED:
                                    # is the target the right item to unlock the item?
                                    if item.GetRequiresToUnlock() == command.target:
                                        # Yep, so unlock
                                        item.SetLocked(False)
                                        print(f"You {command.verb} the {command.obj}.")
                                    else:
                                        # Wrong item to unlock
                                        print(f"You can't {command.verb} the {command.obj} with the {command.target}...")
                                else:
                                    # Target item not here
                                    print(f"I don't see a {command.target} anywhere!")
                            else:
                                # Item already unlocked
                                print(f"You can't {command.verb} a {command.verb}ed {command.obj}..")
                        else:
                            # Not a container
                            print(f"You can't {command.verb} the {command.obj}!")
                    else:
                        # Item to be unlocked is not here
                        print(f"I don't see a {command.obj} anywhere!")
                else:
                    print(f"Sorry, how do you want to {command.verb} the {command.obj}?")
            else:
                # No target specified
                print(f"Sorry, I don't understand. What do you want to use to {command.verb} the {command.obj}?")
        else:
            # No valid obj
            print(f"Sorry, I don't understand what you want to {command.obj}...")

    def HitItem(self, command):
        # Just do this for now
        print(f"You {command.verb} the {command.obj}. That was a waste of time, nothing happened.")
        
    def HitBlockedExit(self, command):
        # Is the exit the player is trying to hit even here?
        blocked_exit_dict = self._location.GetBlockedExit()
        if "name" in blocked_exit_dict and blocked_exit_dict["name"] == command.obj:
            # Yep, valid prep?
            if command.prep == "with" or command.prep == "using":
                # Is the player using the right item?
                if command.target == blocked_exit_dict["target"]:
                    # Yep. Add new exits
                    exits = blocked_exit_dict["exits"]
                    for direction in exits:
                        self._location.AddExit(direction, exits[direction])

                    # Update blocked exit description
                    blocked_exit_dict["desc"] = blocked_exit_dict["alt_desc"]

                    # Update player
                    effect = blocked_exit_dict["effect"]
                    print(f"You {command.verb} the {command.obj} using the {command.target}. {effect}")
                else:
                    # Incorrect target specified to unblock
                    print(f"You {command.verb} the {command.obj}. It has no effect.")
            else:
                # Invalid prep specified
                print(f"Sorry, how do you want to {command.verb} the {command.obj}?")
        else:
            # Blocked exit not here
            print(f"I don't see a {command.obj} here for you to {command.verb}...")

    def Hit(self, command):
        # Did we get a valid object name?
        if command.obj is not None:
            # Player is trying to hit an item?
            if self._parser.IsItem(command.obj):
                self.HitItem(command)
            # Player is trying to hit a blocked exit?
            elif self._parser.IsBlockedExit(command.obj):
                self.HitBlockedExit(command)
            else:
                # Not an item or a blocked exit
                print(f"You want to {command.verb} what? That makes no sense")
        else:
            # No valid obj specified
            print(f"Sorry, I don't understand what you want to {command.verb}...")


    def DoCommand(self, command):
        # What's our verb
        # (Not using match/case here as it requires >= 3.10)
        if command.verb == "go":
            self.Go(command)
        if command.verb == 'hit' or command.verb == "break":
            self.Hit(command)
        elif command.verb == "get":
            self.Get(command)
        elif command.verb == "drop":
            self.Drop(command)
        elif command.verb == "open":
            self.Open(command)
        elif command.verb == "close":
            self.Close(command)
        elif command.verb == "lock":
            self.Lock(command)
        elif command.verb == "unlock":
            self.Unlock(command)
        elif command.verb == "examine":
            self.Examine(command)
        elif command.verb == "inventory":
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
            if command.verb == None:
                print("Sorry, I don't understand what you said ...")
            elif command.verb == "quit":
                print("You'll be back!")
                self._alive = False
            else:
                self.DoCommand(command)
