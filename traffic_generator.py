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

"""
class MaxHeap:
    def __init__(self):
        self.h = []

    def push(self, x):
        self.h.append(x)
        i = len(self.h) - 1
        while i > 0:
            p = (i - 1) // 2
            if self.h[p] >= self.h[i]:
                break
            self.h[p], self.h[i] = self.h[i], self.h[p]
            i = p

    def pop(self):
        if not self.h:
            return None
        self.h[0], self.h[-1] = self.h[-1], self.h[0]
        val = self.h.pop()
        i = 0
        n = len(self.h)

        while True:
            l = 2*i + 1
            r = 2*i + 2
            largest = i

            if l < n and self.h[l] > self.h[largest]:
                largest = l
            if r < n and self.h[r] > self.h[largest]:
                largest = r
            if largest == i:
                break

            self.h[i], self.h[largest] = self.h[largest], self.h[i]
            i = largest

        return val
""" 