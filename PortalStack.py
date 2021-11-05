class PortalStack:
    def __init__(self):
        self._head = None
        self._size = 0
    
    def __len__(self):
        return self._size

    def is_empty(self):
        if self._size == 0:
            return True
        else:
            return False

    def push(self, portal):
        if self._size > 0:
            self._head.portal.image = "portal.ppm" # set old portal image to not flashing in case it was
        temp = self._head # saves current head
        self._head = _StackNode(portal) # assigns head to new node
        self._head.next = temp # assigns new node (head) next to old head
        self._size += 1 # increments size
        
    def pop(self):
        if self._size == 0:
            return None # if empty, return None
        temp = self._head # saves current head
        self._head = temp.next # assign head to next node
        temp.portal.image = "portal.ppm" # set old portal image to not flashing in case it was
        self._size -= 1 # decrement size
        return temp.portal # return old head data

    def get_head(self):
        return self._head.portal
        
class _StackNode:
    def __init__(self, portal):
        self.portal = portal
        self.next = None
    