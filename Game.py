""" Game to play 'Lost Rovers'. This is the file you edit.
To make more ppm files, open a gif or jpg in xv and save as ppm raw.
Put the three ADTs in their own files.
"""
from gameboard import *
from random import *

class Game:
    SIZE = 15 # rooms are 15x15
    def __init__(self):
        # put other instance variables here
        self.gui = GameBoard("Lost Rover", self, Game.SIZE)

    def start_game(self):
        self.gui.run()

    def get_rover_image(self):
        """ Called by GUI when screen updates.
            Returns image name (as a string) of the rover.
		(Likely 'rover.ppm') """
        return 'rover.ppm'

    def get_rover_location(self):
        """ Called by GUI when screen updates.
            Returns location (as a Point). """
        # Your code goes here, this code is just an example
        return Point(3,7)

    def get_image(self, point):
        """ Called by GUI when screen updates.
            Returns image name (as a string) or None for the
		part, ship component, or portal at the given
		coordinates. ('engine.ppm' or 'cake.ppm' or
		'portal.ppm', etc) """
        # Your code goes here, this code is just an example
        r = randint(0,25)
        if r == 0:
            return 'cake.ppm'
        elif r == 1:
            return 'engine.ppm'
        elif r == 2:
            return 'portal.ppm'
        else:
            return None

    def go_up(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        pass # Your code goes here

    def go_down(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        pass # Your code goes here

    def go_left(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        pass # Your code goes here

    def go_right(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        pass # Your code goes here

    def show_way_back(self):
        """ Called by GUI when button clicked.
            Flash the portal leading towards home. """
        pass # Your code goes here

    def get_inventory(self):
        """ Called by GUI when inventory updates.
            Returns entire inventory (as a string).
		3 cake
		2 screws
		1 rug
	  """
        pass # Your code goes here

    def pick_up(self):
        """ Called by GUI when button clicked.
		If rover is standing on a part (not a portal
		or ship component), pick it up and add it
		to the inventory. """
        pass # Your code goes here

    def get_current_task(self):
        """ Called by GUI when task updates.
            Returns top task (as a string).
		'Fix the engine using 2 cake, 3 rugs' or
		'You win!'
 	  """
        pass # Your code goes here

    def perform_task(self):
        """ Called by the GUI when button clicked.
            If necessary parts are in inventory, and rover
            is on the relevant broken ship piece, then fixes
            ship piece and removes parts from inventory. If
            we run out of tasks, we win. """
        pass # Your code goes here

    # Put other methods here as needed.

# Put other classes here or in other files as needed.

""" Launch the game. """
g = Game()
g.start_game() # This does not return until the game is over
