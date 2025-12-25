import socket
import json

# Socket configuration
HEADER = 64
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

class TrafficSimulator:
    """Client that receives traffic data and will display it"""
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
    
    def connect(self):
        """Connect to traffic generator server"""
        try:
            self.client.connect(ADDR)
            print(f"[CONNECTED] Connected to server at {SERVER}:{PORT}")
            return True
        except Exception as e:
            print(f"[ERROR] Could not connect to server: {e}")
            return False
    
    def receive_data(self):
        """Receive traffic data from server"""
        try:
            # Receive message length
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length.strip())
                
                # Receive actual message
                msg = self.client.recv(msg_length).decode(FORMAT)
                data = json.loads(msg)
                return data
        except Exception as e:
            print(f"[ERROR] Receiving data: {e}")
            return None
    
    def display_data(self, data):
        """Display received traffic data (placeholder for pygame)"""
        if data:
            print("\n" + "="*70)
            print("RECEIVED TRAFFIC DATA")
            print("="*70)
            print(f"Timestamp: {data.get('timestamp', 'N/A')}")
            print(f"Current Green Lane: {data.get('current_green_lane', 'N/A')}")
            print("\nQueue Status:")
            
            queues = data.get('queues', {})
            for road in ['A', 'B', 'C', 'D']:
                print(f"\nRoad {road}:")
                for i in [1, 2, 3]:
                    lane = f"{road}L{i}"
                    if lane in queues:
                        queue_info = queues[lane]
                        size = queue_info.get('size', 0)
                        priority = queue_info.get('priority', 0)
                        status = "🟢 GREEN" if lane == data.get('current_green_lane') else "🔴 RED"
                        print(f"  {lane}: {size:2d} vehicles | Priority: {priority} | {status}")
            print("="*70)
    
    def run(self):
        """Main loop to receive and display data"""
        if not self.connect():
            return
        
        self.running = True
        print("\n[SIMULATOR] Waiting for traffic data...\n")
        
        try:
            while self.running:
                data = self.receive_data()
                if data:
                    self.display_data(data)
                    # Here is where pygame rendering would happen
                else:
                    break
        except KeyboardInterrupt:
            print("\n[STOPPED] Simulator stopped by user")
        finally:
            self.client.close()
            print("[DISCONNECTED] Closed connection to server")


if __name__ == "__main__":
    simulator = TrafficSimulator()
    simulator.run()