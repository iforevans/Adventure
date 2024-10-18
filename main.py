from Adventure import *

class Game(object):
    def __init__(self):
        self._alive = True
        self._locations = []
        self._location_id = 0
        self._location = None
        self._items = {}

        # Create location 0
        location = Location(0, "You are inside a cabin in the woods. There is nothing here.")
        location.SetExits(-1, -1, -1, -1, -1, 1, -1, -1)
        self._locations.append(location)

        # Create location 1
        location = Location(1, "You are outside a small, wooden cabin in the woods.")
        location.SetExits(-1, -1, -1, -1, 0, -1, -1, -1)
        self._locations.append(location)

        # Set starting location
        self._location = self._locations[self._location_id]

    def DoCommand(self, command):
        # Assume the command is a move for now
        new_location_id = self._location.Move(command)
        if new_location_id != -1:
            self._location_id = new_location_id
            self._location = self._locations[self._location_id]
        else:
            print(f"You can't go {command}!")


    # Main run method
    def run(self):
        while (self._alive):
            # Tell the player where they are
            self._location.Describe()

            # What do they want to do?
            command = input("What next? ")

            # Parse the command (KISS for now)
            if command == "quit":
                # We're done
                print("You'll be back!")
                self._alive = False
            else:
                self.DoCommand(command)


# Create Game object and run the game
if __name__ == "__main__":
    game = Game()
    game.run()
