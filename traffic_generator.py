import random
from datetime import datetime
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

class Vehicle:
    """Simple Vehicle class"""
    def __init__(self, vehicle_id, lane):
        self.id = vehicle_id
        self.lane = lane
        self.timestamp = datetime.now().isoformat()
    
    def __repr__(self):
        return f"{self.id}"


class TrafficSystem:
    """Traffic system managing 12 lane queues"""
    
    def __init__(self):
        # Define all 12 lanes (3 lanes per road, 4 roads)
        self.lanes = [
            "AL1", "AL2", "AL3",  # Road A lanes
            "BL1", "BL2", "BL3",  # Road B lanes
            "CL1", "CL2", "CL3",  # Road C lanes
            "DL1", "DL2", "DL3"   # Road D lanes
        ]
        
        # Create a VehicleQueue for each lane
        self.queues = {
            lane: VehicleQueue(lane) for lane in self.lanes
        }
        
        self.vehicle_counter = 0
    
    def vehicle_adder(self):
        """
        Randomly adds a vehicle to each of the 12 queues
        Uses random probability to decide if a vehicle should be added
        """
        for lane in self.lanes:
            # Random probability: 30% chance to add vehicle to each lane
            if random.random() < 0.3:
                self.vehicle_counter += 1
                vehicle = Vehicle(f"V{self.vehicle_counter:04d}", lane)
                self.queues[lane].enqueue(vehicle)
                print(f"Added {vehicle.id} to {lane} [Size: {self.queues[lane].size()}]")
