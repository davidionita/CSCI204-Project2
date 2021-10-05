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

        self.rover = Rover(Point(random.randint(0, Game.SIZE), random.randint(0, Game.SIZE)))

        self.room = Room(Game.SIZE)
        
        self.room.set_location(Point(6,6), ShipComponent(Point(6,6), "cabinbroken.ppm", "cabin", True))     # broken cabin @ 6,6
        self.room.set_location(Point(7,6), ShipComponent(Point(7,6), "enginebroken.ppm", "engine", True))   # broken engine @ 7,6
        self.room.set_location(Point(6,7), ShipComponent(Point(6,7), "cabin.ppm", "cabin", False))          # fixed cabin @ 6,7
        self.room.set_location(Point(7,7), ShipComponent(Point(7,7), "engine.ppm", "engine", False))        # fixed engine @ 7,7
        self.room.set_location(Point(8,7), ShipComponent(Point(8,7), "exhaustbroken.ppm", "exhaust", True)) # broken exhaust @ 8,7
        self.room.set_location(Point(8,8), ShipComponent(Point(8,8), "cabinbroken.ppm", "cabin", True))     # broken cabin @ 8,8
         
        numPortals = random.randint(2, 7)
        for i in range(numPortals):
          position = Point(random.randint(0, Game.SIZE),random.randint(0, Game.SIZE))
          while self.room.get_location(position) is None:
            position = Point(random.randint(0, Game.SIZE),random.randint(0, Game.SIZE))
          self.room.set_location(position, Portal(position))

        PARTS = ["bagel", "cake", "lettuce", "gear", "screw"]
        distinctParts = [None, None, None, None]
        numParts = random.randint(7, 13)
        for i in range(numParts):
          position = Point(random.randint(0, Game.SIZE),random.randint(0, Game.SIZE))
          while self.room.get_location(position) is None:
            position = Point(random.randint(0, Game.SIZE),random.randint(0, Game.SIZE))

          # randint for each tpye of part 
          
        
          kindNum = randint(0, 5)
          if i<4: # for the first 4 parts make sure they're distinct THEN randomize type for rest of them
            kindNum = randint(0, 5)
            while kindNum in distinctParts:
              kindNum = randint(0, 5)
            distinctParts[i] = kindNum

            self.room.set_location(position, Part(position, PARTS[kindNum]+".ppm", PARTS[kindNum]))
          else:
            kindNum = randint(0, 5)
            self.room.set_location(position, Part(position, PARTS[kindNum]+".ppm", PARTS[kindNum]))


    def start_game(self):
        self.gui.run()

    def get_rover_image(self):
        """ Called by GUI when screen updates.
            Returns image name (as a string) of the rover.
		(Likely 'rover.ppm') """
        return self.rover.image

    def get_rover_location(self):
        """ Called by GUI when screen updates.
            Returns location (as a Point). """
        return self.rover.position

    def get_image(self, point):
        """ Called by GUI when screen updates.
            Returns image name (as a string) or None for the
		part, ship component, or portal at the given
		coordinates. ('engine.ppm' or 'cake.ppm' or
		'portal.ppm', etc) """
        item = self.room.set_location(point)
        if item is None:
            return None
        elif not isinstance(item, Rover):
            return item.image

    def go_up(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.rover.position.y == 0:
          print("Hit wall, cannot move up")
        else:
          self.rover.position.y -= 1

    def go_down(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.rover.position.y == Game.SIZE-1:
          print("Hit wall, cannot move down")
        else:
          self.rover.position.y += 1

    def go_left(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.rover.position.x == 0:
          print("Hit wall, cannot move left")
        else:
          self.rover.position.x -= 1

    def go_right(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.rover.position.x == Game.SIZE-1:
          print("Hit wall, cannot move right")
        else:
          self.rover.position.x += 1

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
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class StaticItem:
  def __init__(self, position, image):
    self.position = position
    self.image = image
    # static items cannot overlap

class Portal(StaticObject):
  def __init__(self, position, image="portal.pmm"):
    super().__init__(position, image)
    # at least 2 portals, random locations and #>2

class Part(StaticObject):
  def __init__(self, position, image, kind):
    super().__init__(position, image)
    self.kind = kind
    # bagel, cake, gear, lettuce, screw -- at least 4 kinds, at least 7 - 12 total, random locations, type, and #>

class ShipComponent(StaticObject):
  def __init__(self, position, image, kind, broken):
    super().__init__(position, image)
    self.kind = kind
    self.broken = broken

class Room:
  def __init__(self, size):
    self.size = size
    
    # use list comprehension to make a 2D array full of None
    self.board = [[None for x in range(size)] for x in range(size)]
    # board can be indexed by [Point.y][Point.x] because it is [row, column]

  def get_location(self, position):
    return self.board[position.y][position.x]

  def set_location(self, position, item):
    self.board[position.y][position.x] = item

class Rover:
  def __init__(self, position, image="rover.ppm"):
    self.position = position
    self.image = image

""" Launch the game. """
g = Game()
g.start_game() # This does not return until the game is over
