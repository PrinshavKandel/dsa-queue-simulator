class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class VehicleQueue:
    def __init__(self, lane_name):
        self.lane_name = lane_name
        self.front = None
        self.rear = None
        self._size = 0
        self.total_vehicles_processed = 0
    
    def enqueue(self, vehicle):
        new_node = Node(vehicle)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
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
    
    def is_empty(self):
        return self.front is None
    
    def size(self):
        return self._size
    
    def get_all_vehicles(self):
        """Return list of all vehicles in queue"""
        vehicles = []
        current = self.front
        while current:
            vehicles.append(current.data)
            current = current.next
        return vehicles
class LaneNode:
    def __init__(self, lane_name, priority=0):
        self.lane_name = lane_name
        self.priority = priority
    
    def __repr__(self):
        return f"LaneNode({self.lane_name}, priority={self.priority})"


class LanePriorityQueue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, lane_node):
        self.queue.append(lane_node)
        self._sort_by_priority()
    
    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        return None
    
    def update_priority(self, lane_name, new_priority):
        for node in self.queue:
            if node.lane_name == lane_name:
                node.priority = new_priority
                self._sort_by_priority()
                return True
        return False
    
    def get_priority(self, lane_name):
        for node in self.queue:
            if node.lane_name == lane_name:
                return node.priority
        return None
    
    def _sort_by_priority(self):
        self.queue.sort(key=lambda x: x.priority, reverse=True)
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
    def get_all_lanes(self):
        return list(self.queue)
    
    def __repr__(self):
        return f"LanePriorityQueue(size={self.size()})"

