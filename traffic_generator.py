import random
from datetime import datetime
import socket
import threading 
HEADER = 64
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"{addr} is connected")
    connected = True

    while connected:
        message_length = conn.recv(HEADER).decode(FORMAT)

        if message_length:
            true_length = int(message_length)
            msg = conn.recv(true_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")

    conn.close() 

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[Establishing connection between traffic_generator.py and simulator.py, please wait...]")
start()


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
        
        # Create Lane Priority Queue
        self.lane_priority_queue = LanePriorityQueue()
        self._initialize_lane_priority_queue()
        
        self.vehicle_counter = 0
    
    def _initialize_lane_priority_queue(self):
        """Initialize priority queue with all lanes at same priority (0)"""
        for lane in self.lanes:
            lane_node = LaneNode(lane, priority=0)
            self.lane_priority_queue.enqueue(lane_node)
    
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
        
        # Check AL2 priority condition after adding vehicles
        self.check_priority_condition()
    
    def check_priority_condition(self):
        """
        Check AL2 priority condition:
        - If AL2 has > 10 vehicles → set highest priority (10)
        - If AL2 has < 5 vehicles → reset to normal priority (0)
        """
        al2_size = self.queues["AL2"].size()
        
        if al2_size > 10:
            self.lane_priority_queue.update_priority("AL2", priority=10)
        elif al2_size < 5:
            self.lane_priority_queue.update_priority("AL2", priority=0)
    
    def process_traffic_lights(self, time_per_vehicle=2):
        """
        Process traffic lights based on lane priority queue
        Serves lanes in priority order, handling green light timing
        """
        # Get copy of all lanes sorted by priority
        lanes_to_serve = self.lane_priority_queue.get_all_lanes()
        
        for lane_node in lanes_to_serve:
            lane = lane_node.lane_name
            
            # Skip if queue is empty
            if self.queues[lane].is_empty():
                continue
            
            # Check if this is priority lane (AL2 with priority > 0)
            if lane == "AL2" and lane_node.priority > 0:
                # Priority lane: serve until < 5 vehicles
                while self.queues[lane].size() >= 5:
                    self.queues[lane].dequeue()
            else:
                # Normal lanes: calculate green light time based on average
                normal_lanes = [ln.lane_name for ln in lanes_to_serve if ln.priority == 0]
                
                if normal_lanes:
                    green_time = self.calculate_green_light_time(normal_lanes, time_per_vehicle)
                    self.serve_lane(lane, green_time, time_per_vehicle)
        # Update priority after serving
        self.check_priority_condition()
    
    def run(self, interval=1.0, cycles=10):
        """
        Main execution loop
        Continuously generates vehicles and processes traffic lights
        
        Args:
            interval: Time delay between cycles (seconds)
            cycles: Number of cycles to run (None for infinite)
        """
        import time
        
        cycle_count = 0
        
        try:
            while True:
                if cycles is not None and cycle_count >= cycles:
                    break
                
                cycle_count += 1
                print(f"\n=== Cycle {cycle_count} ===")
                
                # Step 1: Generate new vehicles
                print("Generating vehicles...")
                self.vehicle_adder()
                
                # Step 2: Process traffic lights and serve vehicles
                print("\nProcessing traffic lights...")
                self.process_traffic_lights()
                
                # Step 3: Display current status
                print(f"\nQueue sizes after cycle {cycle_count}:")
                for lane in self.lanes:
                    size = self.queues[lane].size()
                    priority = self.lane_priority_queue.get_priority(lane)
                    print(f"  {lane}: {size} vehicles (priority: {priority})")
                
                # Wait before next cycle
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nTraffic system stopped by user.")
        
        print(f"\nTotal cycles completed: {cycle_count}")
        print(f"Total vehicles generated: {self.vehicle_counter}")
    
    def calculate_green_light_time(self, normal_lanes, time_per_vehicle=2):
        """
        Calculate green light duration based on average vehicles in normal lanes
        Formula: |V| = (1/n) * Σ|Li|
        Green light time = |V| * t
        
        Args:
            normal_lanes: List of lane names to consider
            time_per_vehicle: Time (seconds) required for one vehicle to pass
        
        Returns:
            float: Green light duration in seconds
        """
        n = len(normal_lanes)
        if n == 0:
            return 0
        
        # Calculate total vehicles across all normal lanes
        total_vehicles = sum(self.queues[lane].size() for lane in normal_lanes)
        
        # Average vehicles to serve
        vehicles_to_serve = total_vehicles / n
        
        # Total green light time
        green_time = vehicles_to_serve * time_per_vehicle
        
        return green_time
    
    def serve_lane(self, lane, green_light_time, time_per_vehicle=2):
        """
        Dequeue vehicles from a lane during green light
        
        Args:
            lane: Lane name to serve
            green_light_time: Duration of green light in seconds
            time_per_vehicle: Time for one vehicle to pass
        
        Returns:
            int: Number of vehicles served
        """
        vehicles_to_serve = int(green_light_time / time_per_vehicle)
        vehicles_served = 0
        
        for _ in range(vehicles_to_serve):
            if not self.queues[lane].is_empty():
                self.queues[lane].dequeue()
                vehicles_served += 1
            else:
                break
        
        return vehicles_served


class LaneNode:
    """Node representing a lane with priority"""
    def __init__(self, lane_name, priority=0):
        self.lane_name = lane_name
        self.priority = priority
    
    def __repr__(self):
        return f"LaneNode({self.lane_name}, priority={self.priority})"


class LanePriorityQueue:
    """
    Priority Queue for managing lane/light serving order
    Higher priority value = served first
    Implemented using Python list with manual sorting
    """
    def __init__(self):
        self.queue = []  # List of LaneNode objects
    
    def enqueue(self, lane_node):
        """
        Add lane to priority queue
        Time Complexity: O(n log n) due to sorting
        """
        self.queue.append(lane_node)
        self._sort_by_priority()
    
    def dequeue(self):
        """
        Remove and return highest priority lane
        Time Complexity: O(1)
        """
        if not self.is_empty():
            return self.queue.pop(0)
        return None
    
    def peek(self):
        """
        View highest priority lane without removing
        Time Complexity: O(1)
        """
        if not self.is_empty():
            return self.queue[0]
        return None
    
    def update_priority(self, lane_name, new_priority):
        """
        Update priority of a specific lane
        Time Complexity: O(n log n)
        """
        for node in self.queue:
            if node.lane_name == lane_name:
                node.priority = new_priority
                self._sort_by_priority()
                return True
        return False
    
    def get_priority(self, lane_name):
        """Get current priority of a lane"""
        for node in self.queue:
            if node.lane_name == lane_name:
                return node.priority
        return None
    
    def _sort_by_priority(self):
        """Sort queue by priority (descending - highest first)"""
        self.queue.sort(key=lambda x: x.priority, reverse=True)
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self.queue) == 0
    
    def size(self):
        """Get number of lanes in queue"""
        return len(self.queue)
    
    def get_all_lanes(self):
        """Return all lane nodes"""
        return list(self.queue)
    
    def __repr__(self):
        return f"LanePriorityQueue(size={self.size()})"