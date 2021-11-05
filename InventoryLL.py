class InventoryLL:
    def __init__(self):
        self._head = None
        self._size = 0
    
    def __len__(self):
        return self._size

    def __str__(self):
        stringBuilder = "" # start string as empty
        node = self._head
        for i in range(self._size): # loop for size of LL
            stringBuilder += node.name + " " + str(node.count) + "\n" # add part name and count to string then new line
            node = node.next # iterate to next node in LL
        return stringBuilder

    def add(self, part):
        node = self._head # assign starting position as head of LL
        for i in range(self._size): # loop for size of LL
            if node.name == part:
                node.count += 1 # if part already in LL, increment count property
                return # exit function
            node = node.next # iterate to next node in LL
        
        # Below runs if list is empty or part not in LL
        node = self._head # resassign node to head
        self._head = _InventoryNode(part, node) # sets head to newly created node, with next prop set to the previous head
        self._size += 1 # increments size
        
    def remove(self, part, amount): # Realized this wasn't necessary (yet) after implementing it ._.
        prevnode = None # saves prevnode if we delete a node
        node = self._head # assigns starting position as head of LL
        for i in range(self._size): # loop for size of LL
            if node.name == part and amount == node.count: 
                node.count -= 1
                # Below conditionals remove node from LL if 0 parts in inventory
                if prevnode is None and node.count == 0: # checks if we are at the head of LL
                    self._head = node.next # sets head to next node
                    self._size -= 1
                elif node.count == 0:
                    prevnode.next = node.next # sets previous next to next node
                    self._size -= 1
                return node.name # returns item to confirm removal
            elif node.name == part:
                node.count -= amount
            prevnode = node # sets prevnode to current node
            node = node.next # iterate to next node in LL
        return None # returns None because, if reached this, item is not in inventory

    def get_parts_dict(self):
        node = self._head
        parts_dict = {}
        for i in range(self._size): # loop for size of LL
            parts_dict[node.name.lower()] = node.count
            node = node.next # iterate to next node in LL
        return parts_dict
        
class _InventoryNode:
    def __init__(self, name, next=None):
        self.name = name
        self.count = 1
        self.next = next # assigns next to passed-in node, or None if nothing passed
    