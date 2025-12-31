**This project (dsa-queue-simulator) contains a real time traffic simulation and management using the Queue and Priority Queue data structure to manage a 4 road intersection system. This project is built with the pygame module and interconnected through python socket programming.**

---

**Important:**
Running the program is achieved by running the programs, traffic_generator.py and simulator.py simultaniously. One way to do that would be by running the command : "python 
traffic_generator.py & python simulator.py" in git-bash.

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
** Socket Architecture**

| Component | Server (Generator) | Client (Simulator) |
|-----------|-------------------|-------------------|
| **Responsibilities** | - Traffic Generation<br>- Queue Management<br>- Priority Processing | - Pygame Display<br>- Vehicle Rendering<br>- Light Visualization |
| **Network** | Port: 5050 | Connects to Server |
| **Communication** | TCP Socket ← → JSON Data Broadcast |

---

***A description of the class Methods(functions) used:**

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
1.move(light_state) - Updates car position based on light state
2.check_collision_ahead(other_cars) - Prevents cars from colliding
3.should_stop_at_red(light_state) - Checks if car should stop at red light
4.has_passed_intersection() - Determines if car has crossed intersection

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
