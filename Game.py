# David Ionita & Ethan Platock
# Project 2 Phase 5
# 11/03/2021
# Professor Dancy

""" Game to play 'Lost Rovers'. This is the file you edit.
To make more ppm files, open a gif or jpg in xv and save as ppm raw.
Put the three ADTs in their own files.
"""
from gameboard import *
from random import *
from InventoryLL import *
from PortalStack import *
from TasksCircularQ import *

class Game:
    SIZE = 15 # rooms are 15x15
    def __init__(self):
        # put other instance variables here
        self.gui = GameBoard("Lost Rover", self, Game.SIZE)

        self.rover = Rover(Point(randint(0, Game.SIZE-1), randint(0, Game.SIZE-1)))

        self.steps = 0

        self.broken = ["cabin", "cabin", "engine", "exhaust"]
        self.PARTS = ["bagel", "cake", "lettuce", "gear", "screw"]

        self.portals = PortalStack() # stack to push and pop from
        
        self.current_room = Room(Game.SIZE, True) # current_room tracks the room the rover is in and displayed on the screen

        self.inventory = InventoryLL()

        self.tasks = TasksCircularQ(4)
        self.create_task()

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
        item = self.current_room.get_location(point)
        
        if item is None:
            return None
        else:
            return item.image

    def go_up(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.tasks.isempty() or self.tasks.peek() == "You died!":
            return
        if self.rover.position.y == 0:
          print("Hit wall, cannot move up")
        else:
          self.rover.position.y -= 1
          new_location = self.current_room.get_location(self.rover.position)
          if isinstance(new_location, Portal): self.teleport(new_location)
          self.handle_steps()


    def go_down(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.tasks.isempty() or self.tasks.peek() == "You died!":
            return
        if self.rover.position.y == Game.SIZE-1:
          print("Hit wall, cannot move down")
        else:
          self.rover.position.y += 1
          new_location = self.current_room.get_location(self.rover.position)
          if isinstance(new_location, Portal): self.teleport(new_location)
          self.handle_steps()

    def go_left(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.tasks.isempty() or self.tasks.peek() == "You died!":
            return
        if self.rover.position.x == 0:
          print("Hit wall, cannot move left")
        else:
          self.rover.position.x -= 1
          new_location = self.current_room.get_location(self.rover.position)
          if isinstance(new_location, Portal): self.teleport(new_location)
          self.handle_steps()

    def go_right(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.tasks.isempty() or self.tasks.peek() == "You died!":
            return
        if self.rover.position.x == Game.SIZE-1:
          print("Hit wall, cannot move right")
        else:
          self.rover.position.x += 1
          new_location = self.current_room.get_location(self.rover.position)
          if isinstance(new_location, Portal): self.teleport(new_location)
          self.handle_steps()

    def teleport(self, portal):
      """ Called by game when rover stands on portal.
      If rover is standing on a a portal, travel to 
      connecting room.  Portal is only linked between
      two rooms.
      """
      #if old and have NO new, then create new and go to it
      if portal.current == "old" and portal.room_new is None:
        self.portals.push(portal)
        portal.room_new = Room(Game.SIZE, False, portal)
        self.current_room = portal.room_new
        portal.current = "new"
        
      #elif old and have new, then go to it
      elif portal.current == "old" and portal.room_new is not None:
        self.portals.push(portal)
        self.current_room = portal.room_new
        portal.current = "new"

      #elif new, then go back to old
      else:
        old_portal = self.portals.pop()
        self.current_room = portal.room_old
        portal.current = "old"

    def show_way_back(self):
        """ Called by GUI when button clicked.
            Flash the portal leading towards home. """
        if not self.portals.is_empty():
            self.portals.get_head().image = "portal-flashing.ppm"

    def get_inventory(self):
        """ Called by GUI when inventory updates.
            Returns entire inventory (as a string).
		3 cake
		2 screws
		1 rug
	  """
        return str(self.inventory)

    def pick_up(self):
        """ Called by GUI when button clicked.
		If rover is standing on a part (not a portal
		or ship component), pick it up and add it
		to the inventory. """
        roverPos = self.rover.position
        item = self.current_room.get_location(roverPos)
        if isinstance(item, Part): # checks if item at rover position is a Part (can be picked up)
            self.inventory.add(str(item)) # adds to inventory
            self.current_room.set_location(roverPos, None) # removes from board/GUI

    def handle_steps(self):
        """ Called by step functions to determine if task is created
        """
        if self.current_room.alien.x == self.get_rover_location().x or self.current_room.alien.y == self.get_rover_location().y:
            while not self.tasks.isempty():
                self.tasks.dequeue()
            self.tasks.enqueue("You died!")

        self.steps += 1
        if self.steps % 50 == 0:
            self.create_task()
    
    def create_task(self):
        """ Called initially and by handle_steps function to create a task
        """
        if len(self.broken) == 0:
            print("Exhausted tasks")
            return

        task = {}

        if len(self.broken) > 1:
            task["fix"] = self.broken[randint(0,len(self.broken)-1)]
        else:
            task["fix"] = self.broken[0]
        self.broken.remove(task["fix"])

        parts = self.PARTS[:]
        task["parts"] = {}
        for i in range(3):
            part_type = parts[randint(0, len(parts)-1)]
            parts.remove(part_type)
            task["parts"][part_type] = randint(2, 4)
        self.tasks.enqueue(task)

    def get_current_task(self):
        """ Called by GUI when task updates.
            Returns top task (as a string).
		'Fix the engine using 2 cake, 3 rugs' or
		'You win!'

        current_task dict strucutre...
            {
                "fix" : "engine",
                "parts" : {
                    "cake" : 2,
                    "rugs" : 3
                    }
            }
 	  """
        if self.tasks.isempty():
            return "You win!"
        current_task = self.tasks.peek()
        if current_task == "You died!":
            return "You died!"
        strBuilder = "Fix the %s using " % current_task["fix"]
        for part, amount in current_task["parts"].items(): # iterate sub-dict of quantity + part(s) needed
            strBuilder += str(amount) + " " + part + ", "
        return strBuilder[:-2]

    def perform_task(self):
        """ Called by the GUI when button clicked.
            If necessary parts are in inventory, and rover
            is on the relevant broken ship piece, then fixes
            ship piece and removes parts from inventory. If
            we run out of tasks, we win. """
        current_task = self.tasks.peek()
        current_space = self.current_room.get_location(self.get_rover_location())

        if (not isinstance(current_space, ShipComponent)) or (str(current_space).lower() != current_task["fix"]+"broken"):
            print("Not on proper Ship Component")
            return
        
        current_inv = self.inventory.get_parts_dict()
        for part, amount in current_task["parts"].items():
            if (not part in current_inv.keys()) or (current_inv[part] < amount):
                print("You do not have enough " + part)
                return

        current_space.image = current_task["fix"] + ".ppm"
        
        for part, amount in current_task["parts"].items():
            self.inventory.remove(part, amount)

        self.tasks.dequeue()

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

  def __str__(self):
    return self.image.split(".")[0].capitalize() # gets section of image filename without ".ppm" then capitalizes

class Alien(StaticItem):
  def __init__(self, position, image):
    super().__init__(position, image)

class Portal(StaticItem):
  def __init__(self, position, image, init_room):
    super().__init__(position, image)
    self.room_old = init_room
    self.room_new = None
    self.current = "old"

class Part(StaticItem):
  def __init__(self, position, image, kind):
    super().__init__(position, image)
    self.kind = kind

class ShipComponent(StaticItem):
  def __init__(self, position, image, kind, broken):
    super().__init__(position, image)
    self.kind = kind
    self.broken = broken

class Room:
  def __init__(self, size, first, portal_back=None):
    self.size = size
    self.alien = Point(-1, -1)
    # Use list comprehension to make a 2D array full of None
    self.board = [[None for x in range(size)] for x in range(size)]
    # Board can be indexed by [Point.y][Point.x] because it is [row, column]
    
    if first:
      # Hardcoded ship components
      self.set_location(Point(6,6), ShipComponent(Point(6,6), "cabinbroken.ppm", "cabin", True))     # broken cabin @ 6,6
      self.set_location(Point(7,6), ShipComponent(Point(7,6), "enginebroken.ppm", "engine", True))   # broken engine @ 7,6
      self.set_location(Point(6,7), ShipComponent(Point(6,7), "cabin.ppm", "cabin", False))          # fixed cabin @ 6,7
      self.set_location(Point(7,7), ShipComponent(Point(7,7), "engine.ppm", "engine", False))        # fixed engine @ 7,7
      self.set_location(Point(8,7), ShipComponent(Point(8,7), "exhaustbroken.ppm", "exhaust", True)) # broken exhaust @ 8,7
      self.set_location(Point(8,8), ShipComponent(Point(8,8), "cabinbroken.ppm", "cabin", True))     # broken cabin @ 8,8

      # Random number of portals from 2 to 6
      numPortals = randint(2, 6)
      
    else:
      # Set the OG portal location to make sure it has a spot
      self.set_location(portal_back.position, portal_back)

      self.alien = Point(randint(0, self.size-1), randint(0, self.size-1))
      while self.get_location(self.alien) is not None:
        self.alien = Point(randint(0, self.size-1), randint(0, self.size-1))
      self.set_location(self.alien, Alien(self.alien, "alien.ppm"))

      # Random number of portals from 2 to 5
      numPortals = randint(2, 5)
      pass
    
    
    for i in range(numPortals):
      # Choose random location for portal without a current item on it
      position = Point(randint(0, self.size-1), randint(0, self.size-1))
      while self.get_location(position) is not None:
        position = Point(randint(0, self.size-1), randint(0, self.size-1)) 
      self.set_location(position, Portal(position, "portal.ppm", self))

    # Static list of parts for easy indexing w/ randint
    PARTS = ["bagel", "cake", "lettuce", "gear", "screw"]
    # Helper list to keep track of distinct parts (need at least 4 different parts)
    distinctParts = [None, None, None, None]
    # Random number of parts from 7 to 12
    numParts = randint(7, 12)
    for i in range(numParts):
      # Choose random location for part without a current item on it
      position = Point(randint(0, self.size-1), randint(0, self.size-1))
      while self.get_location(position) is not None:
        position = Point(randint(0, self.size-1), randint(0, self.size-1))
      
      # Random part (0-4 as indexed in the static list)
      kindNum = randint(0, 4)
      if i<4: # For the first 4 parts, make sure they're distinct; THEN randomize the kind/type for rest of them
        kindNum = randint(0, 4)
        # Make sure randomly chosen part is distinct
        while kindNum in distinctParts:
          kindNum = randint(0, 4)
        distinctParts[i] = kindNum
        self.set_location(position, Part(position, PARTS[kindNum]+".ppm", PARTS[kindNum]))
      else:
        kindNum = randint(0, 4)
        self.set_location(position, Part(position, PARTS[kindNum]+".ppm", PARTS[kindNum]))    

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
