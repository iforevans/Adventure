from Adventure import *

def CreateLocations():
    loc_list = []

    # Create location 0
    location = Location(0, "You are inside a cabin in the woods. There is nothing here.")
    location.SetExits(-1, -1, -1, -1, -1, 1, -1, -1)
    loc_list.append(location)

    # Create location 1
    location = Location(1, "You are outside a small, wooden cabin in the woods.")
    location.SetExits(-1, -1, -1, -1, 0, -1, -1, -1)
    loc_list.append(location)

    # return our list of locations
    return loc_list

def ParseCommand(command):
    pass


# Main func
def main():
    # Set players current status
    dead = False

    # Create our locations
    loc_list = CreateLocations()

    # Start in loc 0
    current_loc_id= 0
    current_loc = loc_list[current_loc_id]

    while (not dead):
        # Tell the player where they are
        current_loc.Describe()

        # What do they want to do?
        command = input("What next? ")

        # Parse the command (KISS for now)
        if command == "quit":
            # We're done
            print("You'll be back!")
            dead = True
        else:
            new_loc = current_loc.Move(command)
            if new_loc != -1:
                current_loc = loc_list[new_loc]
            else:
                print(f"You can't go {command}!")


# Call main
if __name__ == "__main__":
    main()
