from array204 import Array

class TasksCircularQ :
	## Initializes queue with underlying array
	def __init__(self, maxs) :
		self.count = 0
		self.maxs = maxs
		self.front = 0
		self.back = maxs - 1
		self.q_array = Array(maxs) #(Assume we have normal array available...)

	## Checks if there are no items in the array
	def isempty(self) :
		return self.count == 0

	## Checks if underlying array is full
	def isfull(self) : 
		return self.count == len(self.q_array)

	def __len__(self) :
		return self.count

	## Add item to back of queue 
	def enqueue(self, item): 
		assert not self.isfull(), "FULL"
		maxs = len(self.q_array)
		self.back = (self.back + 1) % maxs
		self.q_array[self.back] = item
		self.count += 1

	## Remove item from front of queue
	def dequeue(self): #(Big-O) 1
		assert not self.isempty(), "EMPTY"
		item = self.q_array[ self.front ]
		maxs = len(self.q_array)
		self.front = (self.front + 1) % maxs
		self.count -= 1
		return item
    
    ## Return the front of the queue, without removing from underlying array
	def peek(self):
		return self.q_array[self.front]