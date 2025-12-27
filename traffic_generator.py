import random
from datetime import datetime
import time

from queue import VehicleQueue, LanePriorityQueue, LaneNode
from server_socket import SocketServer
class Vehicle:
    """Vehicle with fixed destination based on lane"""
    def __init__(self, vehicle_id, lane):
        self.id = vehicle_id
        self.lane = lane
        self.destination = self._get_destination()
        self.timestamp = datetime.now().isoformat()
    
    def _get_destination(self):

       if self.lane == "AL3":
           return "CL1"
       elif self.lane == "BL3":
           return "DL1"
       elif self.lane == "CL3":
          return "BL1"
       elif self.lane == "DL3":
          return "AL1"
    
    # L2 lanes: 50% straight, 50% left
       elif self.lane == "AL2":
           return random.choice(["BL1", "DL1"])
       elif self.lane == "BL2":
           return random.choice(["AL1", "CL1"])
       elif self.lane == "CL2":
           return random.choice(["DL1", "BL1"])
       elif self.lane == "DL2":
           return random.choice(["CL1", "AL1"])
    
       return None
  
    
    def __repr__(self):
        return f"{self.id}({self.lane}→{self.destination})"


class TrafficSystem:
    def __init__(self):
        # Only L2 and L3 lanes (no L1 - incoming only)
        self.lanes = ["AL2", "AL3", "BL2", "BL3", "CL2", "CL3", "DL2", "DL3"]
        
        self.queues = {lane: VehicleQueue(lane) for lane in self.lanes}
        self.current_green_road = None
        self.green_time_remaining = 0
        self.lane_priority_queue = LanePriorityQueue()
        self._initialize_lane_priority_queue()
        self.vehicle_counter = 0
        self.socket_server = SocketServer()
        self.socket_server.start()
    
    def _initialize_lane_priority_queue(self):
        """Only L2 lanes in priority queue"""
        for lane in ["AL2", "BL2", "CL2", "DL2"]:
            self.lane_priority_queue.enqueue(LaneNode(lane, priority=0))
    
    def vehicle_adder(self):
        """Add vehicles to lanes"""
        for lane in self.lanes:
            probability = 0.7 if lane == "AL2" else 0.3
            if random.random() < probability:
                self.vehicle_counter += 1
                vehicle = Vehicle(f"V{self.vehicle_counter:04d}", lane)
                self.queues[lane].enqueue(vehicle)
                print(f"Added {vehicle.id} to {lane} [Size: {self.queues[lane].size()}]")
        self.check_priority_condition()
    
    def check_priority_condition(self):
        """Check AL2 priority"""
        al2_size = self.queues["AL2"].size()
        if al2_size > 10:
            self.lane_priority_queue.update_priority("AL2", 10)
            print(f"  AL2 PRIORITY (Size: {al2_size})")
        elif al2_size < 5:
            self.lane_priority_queue.update_priority("AL2", 0)
    
    def process_traffic_lights(self):
        """Process traffic lights"""
        if self.current_green_road is None or self.green_time_remaining <= 0:
            self.select_next_green_road()
        
        if self.green_time_remaining > 0:
            self.green_time_remaining -= 1
            self.serve_current_green_road()
    
    def select_next_green_road(self):
        """Select next green road"""
        lanes_to_serve = self.lane_priority_queue.get_all_lanes()
        if not lanes_to_serve:
            return
        
        next_lane = lanes_to_serve[0]
        for lane_node in lanes_to_serve:
            if not self.queues[lane_node.lane_name].is_empty():
                next_lane = lane_node
                break
        
        self.current_green_road = next_lane.lane_name[0]
        
        if next_lane.lane_name == "AL2" and next_lane.priority > 0:
            vehicles_to_serve = max(0, self.queues[next_lane.lane_name].size() - 4)
            self.green_time_remaining = vehicles_to_serve
        else:
            normal_lanes = [ln for ln in lanes_to_serve if ln.priority == 0]
            if normal_lanes:
                total_vehicles = sum(self.queues[ln.lane_name].size() for ln in normal_lanes)
                avg_vehicles = total_vehicles / len(normal_lanes) if normal_lanes else 0
                self.green_time_remaining = int(avg_vehicles)
        
        print(f" Road {self.current_green_road} GREEN (for {self.green_time_remaining} vehicles)")
    
    def serve_current_green_road(self):
        """Serve vehicles from current green road"""
        if not self.current_green_road:
            return
        
        road_lanes = [lane for lane in self.lanes if lane.startswith(self.current_green_road)]
        for lane in road_lanes:
            if not self.queues[lane].is_empty():
                vehicle = self.queues[lane].dequeue()
                print(f"  ✓ {vehicle.id} passed from {lane}")
        
        self.check_priority_condition()
    
    def run(self, interval=1.5, cycles=100):
        """Run simulation"""
        cycle_count = 0
        
        try:
            while True:
                if cycles is not None and cycle_count >= cycles:
                    break
                
                cycle_count += 1
                print(f"\n{'='*60}\nCYCLE {cycle_count}\n{'='*60}")
                
                print("\n Generating vehicles...")
                self.vehicle_adder()
                
                print(f"\n Processing traffic lights...")
                self.process_traffic_lights()
                
                print(f"\n Queue Status:")
                for lane in self.lanes:
                    size = self.queues[lane].size()
                    priority = self.lane_priority_queue.get_priority(lane) or 0
                    status = "  GREEN" if lane[0] == self.current_green_road else "  RED"
                    if priority > 0:
                        status += "  PRIORITY"
                    print(f"  {lane}: {size:2d} vehicles{status}")
                
                # Broadcast to client
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'queues': {
                        lane: {
                            'size': self.queues[lane].size(),
                            'vehicles': [{'id': v.id, 'lane': v.lane, 'destination': v.destination} 
                                       for v in self.queues[lane].get_all_vehicles()[:12]]  # Max 12
                        }
                        for lane in self.lanes
                    },
                    'current_green_road': self.current_green_road,
                    'green_time_remaining': self.green_time_remaining
                }
                self.socket_server.broadcast_data(data)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n Traffic system stopped")
            self.socket_server.stop()
        
        print(f"\n Simulation Complete\nTotal cycles: {cycle_count}\nTotal vehicles: {self.vehicle_counter}")
if __name__ == "__main__":
    traffic_system = TrafficSystem()
    traffic_system.run(interval=0.5, cycles=100)
