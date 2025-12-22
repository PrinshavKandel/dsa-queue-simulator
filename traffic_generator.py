class Node:
    def __init__(self, data):
        self.data = data  # Vehicle object
        self.next = None  # Pointer to next node

class VehicleQueue:
    def __init__(self, lane_name):
        self.lane_name = lane_name
        self.front = None  # Points to first node (head)
        self.rear = None   # Points to last node (tail)
        self._size = 0     # Track size for O(1) access
        self.total_vehicles_processed = 0
    
    def enqueue(self, vehicle):
        new_node = Node(vehicle)
        
        if self.is_empty():
            # If queue is empty, front and rear point to same node
            self.front = new_node
            self.rear = new_node
        else:
            # Add new node at rear and update rear pointer
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1
    
    def dequeue(self):
        if self.is_empty():
            return None
        vehicle = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        self.total_vehicles_processed += 1
        return vehicle
    
    def peek(self):
        if self.is_empty():
            return None
        return self.front.data
    
    def is_empty(self):
        return self.front is None
    
    def size(self):
        return self._size

