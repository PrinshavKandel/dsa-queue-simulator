import random
from datetime import datetime
import socket
import threading 
import json
import time
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

        al2_size = self.queues["AL2"].size()
        
        if al2_size > 10:
            self.lane_priority_queue.update_priority("AL2", priority=10)
        elif al2_size < 5:
            self.lane_priority_queue.update_priority("AL2", priority=0)
    
    def process_traffic_lights(self, time_per_vehicle=2):

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

        vehicles_to_serve = int(green_light_time / time_per_vehicle)
        vehicles_served = 0
        
        for _ in range(vehicles_to_serve):
            if not self.queues[lane].is_empty():
                self.queues[lane].dequeue()
                vehicles_served += 1
            else:
                break
        
        return vehicles_served

class SocketServer:
    """Handles all socket communication for traffic system"""
    
    def __init__(self):
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.connected_clients = []
        self.running = False
    
    def send_to_client(self, conn, data):
        """Send data to a specific client"""
        message = json.dumps(data)
        msg_encoded = message.encode(self.FORMAT)
        msg_length = len(msg_encoded)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        
        try:
            conn.send(send_length)
            conn.send(msg_encoded)
        except:
            pass
    
    def broadcast_data(self, data):
        """Send data to all connected clients"""
        for conn in self.connected_clients[:]:
            try:
                self.send_to_client(conn, data)
            except:
                self.connected_clients.remove(conn)
    
    def handle_client(self, conn, addr):
        """Handle individual client connection"""
        print(f"[NEW CONNECTION] {addr} connected")
        self.connected_clients.append(conn)
        
        try:
            while self.running:
                time.sleep(0.1)
        except:
            pass
        
        if conn in self.connected_clients:
            self.connected_clients.remove(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected")
    
    def start(self):
        """Start listening for client connections"""
        self.running = True
        
        def listen():
            self.server.listen()
            print(f"[LISTENING] Server is listening on {self.SERVER}:{self.PORT}")
            
            while self.running:
                try:
                    conn, addr = self.server.accept()
                    thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                    thread.daemon = True
                    thread.start()
                    print(f"[ACTIVE CONNECTIONS] {len(self.connected_clients)}")
                except:
                    break
        
        server_thread = threading.Thread(target=listen)
        server_thread.daemon = True
        server_thread.start()
    
    def stop(self):
        """Stop the server"""
        self.running = False
        for conn in self.connected_clients:
            conn.close()
        self.server.close()
        print("[SERVER] Stopped")


class LaneNode:
    """Node representing a lane with priority"""
    def __init__(self, lane_name, priority=0):
        self.lane_name = lane_name
        self.priority = priority
    
    def __repr__(self):
        return f"LaneNode({self.lane_name}, priority={self.priority})"


class LanePriorityQueue:

    def __init__(self):
        self.queue = []  # List of LaneNode objects
    
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