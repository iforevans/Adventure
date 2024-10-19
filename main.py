from Adventure import *

class Game(object):
    def __init__(self):
        self._alive = True
        self._locations = []
        self._location = None
        self._carried = {}

        # Create the game map & Items
        self.CreateMap()
        self.CreateItems()

        # Set starting location
        self._location = self._locations[0]

    def CreateMap(self):
        # Create location 0
        location = Location(0, "You are inside a cabin in the woods.")
        location.SetExits(-1, -1, -1, -1, -1, 1, -1, -1)
        self._locations.append(location)

        # Create location 1
        location = Location(1, "You are outside a small, wooden cabin in the woods.")
        location.SetExits(-1, -1, 2, -1, 0, -1, -1, -1)
        self._locations.append(location)

        # Create location 2
        location = Location(2, "You are on a overgrown north/south path in the woods.")
        location.SetExits(1, -1, -1, -1, -1, -1, -1, -1)
        self._locations.append(location)

    def CreateItems(self):
        # Full bottle
        item = Item("bottle", "The bottle is full of water", 1)
        self._locations[0].DropItem(item)

        # Sword
        item = Item("sword", "A rusty old sword.", 3)
        self._locations[1].DropItem(item)

    # Move in a valid direction
    def Move(self, direction):
        new_location_id = self._location.Move(direction)
        if new_location_id != -1:
            self._location = self._locations[new_location_id]
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


# Create Game object and run the game
if __name__ == "__main__":
    game = Game()
    game.run()
