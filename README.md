**This project (dsa-queue-simulator) contains a real time traffic simulation and management using the Queue and Priority Queue data structure to manage a 4 road intersection system. This project is built with the pygame module and interconnected through python socket programming.**

---

**Author:Prinshav Kandel
Computer Science(I)
Roll no. 30**

---

**Important:**
Running the program is achieved by running the programs, traffic_generator.py and simulator.py simultaniously. One way to do that would be by running the command : "python 
traffic_generator.py & python simulator.py" in git-bash.

**Project File Structure**
```
traffic-simulation/
│
├── queue.py                    # Queue data structures implementation
│   ├── Node                    # Linked list node for vehicle storage
│   ├── VehicleQueue            # FIFO queue using singly linked list
│   ├── LaneNode                # Priority queue node for lane management
│   └── LanePriorityQueue       # Priority queue for lane serving order
│
├── traffic_generator.py        # Main traffic generation logic
│   ├── Vehicle                 # Vehicle class with destination logic
│   └── TrafficSystem           # Core traffic management system
│       ├── vehicle_adder()     # Generates vehicles randomly
│       ├── check_priority()    # Monitors AL2 priority condition
│       ├── process_lights()    # Manages traffic light states
│       └── serve_vehicles()    # Dequeues vehicles during green light
│
├── server_socket.py            # Server-side socket communication
│   └── SocketServer            # Handles client connections
│       ├── send_to_client()    # Sends data to specific client
│       ├── broadcast_data()    # Broadcasts to all connected clients
│       ├── handle_client()     # Manages individual client threads
│       └── start()             # Initializes server on port 5050
│
├── client_socket.py            # Client-side socket communication
│   └── SocketClient            # Connects to traffic generator
│       ├── connect()           # Establishes server connection
│       ├── receive_data()      # Continuously receives traffic data
│       └── start()             # Starts client with callback function
│
└── simulator.py                # Pygame visualization client
    ├── Car                     # Vehicle rendering and movement logic
    └── TrafficSimulator        # Main simulation controller
        ├── update_from_data()  # Updates state from server data
        ├── draw()              # Renders traffic visualization
        └── update()            # Handles car movement and physics
```

***File Purposes***

| File | Purpose | Key Components |
|------|---------|----------------|
| **queue.py** | Implements queue data structures for vehicle and lane management | VehicleQueue (linked list FIFO), LanePriorityQueue (array-based) |
| **traffic_generator.py** | Generates traffic, manages queues, processes traffic lights | TrafficSystem orchestrates all traffic logic |
| **server_socket.py** | Server-side network communication | Broadcasts traffic data to connected simulators |
| **client_socket.py** | Client-side network communication | Receives traffic data from generator |
| **simulator.py** | Visual representation using pygame | Renders cars, lanes, and traffic lights in real-time |

## Communication Flow
```
traffic_generator.py  ─┐
                       ├──> Uses queue.py for data structures
                       └──> Uses server_socket.py for broadcasting
                                      │
                                      │ Socket Network (Port 5050)
                                      │
simulator.py ──────────┐              │
                       ├──> Uses client_socket.py for receiving data
                       └──< Receives traffic updates ───────┘
```

***How to Run***
bash
Terminal 1: Start traffic generator (server)
python traffic_generator.py

Terminal 2: Start simulator (client)
python simulator.py


**Note:** Start the traffic generator first, then the simulator will connect automatically.

---

**Demonstration video:** https://youtu.be/dGJtmiF-Mvo

---

**Project Aim:**
1. Server-side traffic generation using linked list-based queues to manage vehicles across 8 active
lanes,
2. Priority queue system that dynamically adjusts lane priorities based on traffic density,
3. Client-side visualization using Pygame to display real-time vehicle movement and traffic light
states.
4. Socket-based communication for real-time data synchronization between server and client

---

**Queue Logic:**

This project uses two queue data structures to manage traffic. The first is a normal vehicle queue that
follows the First In First Out principle and is implemented using a ***singly linked list***.
The second structure is a lane priority queue, implemented using an ***array-based list***, which determines the
order in which lanes are served. Each lane has an associated priority value, and the list is kept sorted so
that the highest-priority lane is served first. Under normal conditions, all lanes have equal priority. When
congestion occurs, such as when lane AL2 exceeds ten vehicles, it is given higher priority and served
immediately. Once its vehicle count drops below five, its priority is reset and normal operation resumes.
Together, the vehicle queues store the cars, while the priority queue decides which lane is served next.

---

**Pygame Implementation for simulation:**

The client-side visualization(simulator.py) uses the Pygame library to display a real-time view of the traffic system. It
initializes a 1000 by 800 pixel window with a 60 FPS loop . A custom made background image shows the
four-way intersection, while vehicle images, scaled to 30 by 30 pixels, are rotated according to their travel
direction. The management of vehicle behavior, including position tracking, movement at two pixels per
frame, collision detection with a 38-pixel safe distance, and smooth turning using distance-based
calculations is managed. Traffic light states are shown by masking inactive red or green lights with black
rectangles drawn over predefined regions.The main loop runs at 60 FPS, handling window events,
updating vehicle positions based on light states.

---

**Socket Programming in python for connection:**

The project uses TCP socket programming to establish client-server communication for real-time data
synchronization between the traffic_generator.py acting as server and simulator.py acting as a client.
This is done in order to enable real-time communication between the traffic generator and the pygame
simulator .The server, implemented in `server_socket.py`, creates a socket that binds to a specific IP address and
port (5050), then listens for incoming client connections. When the simulator connects, the server accepts
the connection and spawns a dedicated thread to handle that client using the, handle_client() method.
Data transmission follows a custom protocol: first, a 64-byte header containing the message length is sent,
followed by the actual JSON-encoded traffic data . The server uses broadcast_data() to send this
information to all connected clients every cycle. On the client side, implemented in client_socket.py, the
simulator establishes a connection to the server, then runs a background thread that continuously receives
data using the same header-message protocol. Upon receiving data, it decodes the JSON and passes it to a
callback function which updates the pygame visualization. This architecture allows the traffic logic and
visualization to run as separate processes, with the socket acting as the communication bridge, enabling
real-time synchronization between traffic generation and visual representation without blocking either
component's execution.

**Socket Architecture:**

| Component | Server (Generator) | Client (Simulator) |
|-----------|-------------------|-------------------|
| **Responsibilities** | - Traffic Generation<br>- Queue Management<br>- Priority Processing | - Pygame Display<br>- Vehicle Rendering<br>- Light Visualization |
| **Network** | Port: 5050 | Connects to Server |
| **Communication** | TCP Socket ← → JSON Data Broadcast |

---

**A description of the class Methods(functions) used:**

***VehicleQueue Functions***

1. enqueue(vehicle) - Adds vehicle to rear of queue (O(1))
2. dequeue() - Removes and returns vehicle from front of queue (O(1))
3. is_empty() - Checks if queue is empty (O(1))
4. size() - Returns current queue size (O(1))
5. get_all_vehicles() - Returns list of all vehicles in queue (O(n))

***LanePriorityQueue Functions***

1. enqueue(lane_node) - Adds lane to priority queue and sorts (O(n log n))
2. dequeue() - Removes highest priority lane (O(1))
3. peek() - Returns highest priority lane without removing (O(1))
4. update_priority(lane_name, new_priority) - Updates priority and re-sorts (O(n log n))
5. get_priority(lane_name) - Gets current priority of a lane (O(n))
6. get_all_lanes() - Returns all lanes sorted by priority (O(1))

***TrafficSystem Functions***

1. vehicle_adder() - Randomly generates vehicles and adds to queues
2. check_priority_condition() - Monitors AL2 size and updates priority
3. process_traffic_lights() - Main traffic light processing loop
4. select_next_green_road() - Determines which road gets green light next
5. serve_current_green_road() - Dequeues vehicles from green road lanes
6. get_broadcast_data() - Prepares data for client broadcast

***Car Movement Functions***
1. move(light_state) - Updates car position based on light state
2. check_collision_ahead(other_cars) - Prevents cars from colliding
3. should_stop_at_red(light_state) - Checks if car should stop at red light
4. has_passed_intersection() - Determines if car has crossed intersection
   

---

**Time Complexity Analysis**
| Operation | Time Complexity |
|-----------|----------------|
| VehicleQueue.enqueue() | O(1) |
| VehicleQueue.dequeue() | O(1) |
| VehicleQueue.size() | O(1) |
| VehicleQueue.get_all_vehicles() | O(n) |
| LanePriorityQueue.enqueue() | O(n log n) |
| LanePriorityQueue.update_priority() | O(n log n) |
| LanePriorityQueue.get_priority() | O(n) |


note: VehicleQueue is implemented differently to LanePriorityQueue, hence the difference in time complexity.
***1. Vehicle Generation***

Vehicle generation runs in O(m) time, where m = 8 represents the number of active lanes. Each lane has a 30 percent probability of generating a vehicle. Creating a vehicle and enqueuing it takes O(1) time per vehicle. Since m is fixed at 8, the total cost becomes O(8), which simplifies to O(1) constant time.

***2. Priority Check***

The priority check operates in O(n log n) time in the worst case. Checking whether lane AL2 exceeds the threshold takes O(1) time. If a priority update is required, it involves reordering priorities, which takes O(n log n), where n = 4 lanes. Since n is very small and constant, the total cost O(4 log 4) simplifies to O(1).

***3. Traffic Light Selection***

Traffic light selection runs in O(n + m) time. Retrieving all lanes from the priority queue takes O(1) time. Identifying non-empty lanes requires O(n) time, where n = 4 lanes, and calculating averages for normal lanes also takes O(n). Since n is constant, the total complexity O(4) simplifies to O(1).

***4. Vehicle Service***

Vehicle servicing takes O(m) time. Dequeuing vehicles from each green lane takes O(1) time per lane. With a maximum of 3 lanes served at a time, the total cost is O(3), which simplifies to O(1).

***5. Data Broadcast***

Data broadcasting runs in O(m × k) time, where m = 8 lanes and k is the number of vehicles per lane with a maximum of 12. Iterating through all vehicles to prepare broadcast data takes O(8 × 12) = O(96), which simplifies to O(1) since both values are constant.

***6. Overall Per-Cycle Complexity***

The overall per-cycle complexity is O(n log n) + O(m × k). Substituting constants gives O(4 log 4) + O(8 × 12) = O(8) + O(96) = O(104), which simplifies to O(1). Therefore, each simulation cycle runs in constant time.

***Total Simulation Complexity***

The total simulation complexity is O(c), where c is the number of cycles. Since each cycle executes in constant time, the total runtime scales linearly with the number of cycles. For example, running 100 cycles results in O(100), which remains linear time complexity.

---

***Refrences:***

---

1)Object Oriented programming essentials in python:


https://www.youtube.com/watch?v=JeznW_7DlB0

---

2)Socket Programming in python:

https://youtu.be/3QiPPX-KeSc?si=pcBCv3WEB7s48JIF
https://www.youtube.com/watch?v=bwTAVGg_kVs

---
3)Pygame essentials

https://www.tutorialspoint.com/pygame/pygame_moving_rectangular_objects.htm
https://www.geeksforgeeks.org/python/how-to-make-a-pygame-window/
https://www.pygame.org/docs/tut/MoveIt.html

---
4)Miscellaneous

https://www.geeksforgeeks.org/python/what-does-the-if-__name__-__main__-do/
