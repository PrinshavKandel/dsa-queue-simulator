import pygame
import sys

from client_socket import SocketClient

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulator")
clock = pygame.time.Clock()
FPS = 60

# Load images
background = pygame.image.load("lanesystem.png").convert_alpha()
car_img = pygame.image.load("car.png").convert_alpha()
car_img = pygame.transform.scale(car_img, (30, 30))

# Lane rectangles
lane_rects = {
    "AL1": pygame.Rect(440, 0, 40, 287), "AL2": pygame.Rect(480, 0, 40, 287), "AL3": pygame.Rect(520, 0, 40, 287),
    "BL1": pygame.Rect(440, 420, 40, 380), "BL2": pygame.Rect(480, 420, 40, 380), "BL3": pygame.Rect(520, 420, 40, 380),
    "DL1": pygame.Rect(0, 284, 420, 40), "DL2": pygame.Rect(0, 340, 420, 40), "DL3": pygame.Rect(0, 387, 420, 40),
    "CL1": pygame.Rect(572, 285, 480, 40), "CL2": pygame.Rect(572, 338, 480, 40), "CL3": pygame.Rect(572, 384, 480, 40),
}

# Traffic light rectangles
light_rects = {
    "A": {"GREEN": pygame.Rect(572, 202, 70, 40), "RED": pygame.Rect(572, 247, 70, 40)},
    "B": {"GREEN": pygame.Rect(347, 475, 70, 36), "RED": pygame.Rect(356, 433, 70, 36)},
    "C": {"GREEN": pygame.Rect(620, 432, 36, 70), "RED": pygame.Rect(579, 437, 36, 64)},
    "D": {"GREEN": pygame.Rect(341, 222, 36, 64), "RED": pygame.Rect(377, 225, 36, 64)},
}

# Stop lines
STOP_LINES = {"A": 280, "B": 425, "C": 555, "D": 415}
BLACK = (0, 0, 0)


class Car:
    def __init__(self, vehicle_data, position_in_queue):
        self.id = vehicle_data['id']
        self.lane = vehicle_data['lane']
        self.destination = vehicle_data['destination']
        self.road = self.lane[0]
        rect = lane_rects[self.lane]
        
        # Calculate spacing: 35 pixels between cars
        spacing = position_in_queue * 35
        
        if self.lane.startswith('A'):
            self.x, self.y = rect.centerx - 15, rect.top + spacing
            self.speed, self.horizontal, self.direction = 2, False, 1
        elif self.lane.startswith('B'):
            self.y = rect.bottom - spacing
            self.x, self.y = rect.centerx - 15, self.y
            self.speed, self.horizontal, self.direction = 2, False, -1
        elif self.lane.startswith('C'):
            self.x = rect.right - spacing
            self.x, self.y = self.x, rect.centery - 15
            self.speed, self.horizontal, self.direction = 2, True, -1
        else:  # D
            self.x, self.y = rect.left + spacing, rect.centery - 15
            self.speed, self.horizontal, self.direction = 2, True, 1
        
        self.stopped = False
        self.passed_intersection = False
        self.turning = False
    
    def should_stop_at_red(self, light_state):
        if self.passed_intersection or light_state != "red":
            return False
        
        if self.road == "A":
            return self.y < STOP_LINES["A"] and self.y > STOP_LINES["A"] - 50
        elif self.road == "B":
            return self.y > STOP_LINES["B"] and self.y < STOP_LINES["B"] + 50
        elif self.road == "C":
            return self.x > STOP_LINES["C"] and self.x < STOP_LINES["C"] + 50
        elif self.road == "D":
            return self.x < STOP_LINES["D"] and self.x > STOP_LINES["D"] - 50
        return False
    
    def has_passed_intersection(self):
        if self.road == "A":
            return self.y > STOP_LINES["A"] + 50
        elif self.road == "B":
            return self.y < STOP_LINES["B"] - 50
        elif self.road == "C":
            return self.x < STOP_LINES["C"] - 50
        elif self.road == "D":
            return self.x > STOP_LINES["D"] + 50
        return False
    
    def move(self, light_state):
        if self.has_passed_intersection():
            self.passed_intersection = True
            if not self.turning and self.destination:
                self._start_turning()
        
        if self.should_stop_at_red(light_state):
            return
        
        if self.turning:
            self._continue_turn()
        else:
            if self.horizontal:
                self.x += self.speed * self.direction
            else:
                self.y += self.speed * self.direction
    
    def _start_turning(self):
        self.turning = True
        dest_rect = lane_rects.get(self.destination)
        if dest_rect:
            self.target_x = dest_rect.centerx - 15
            self.target_y = dest_rect.centery - 15
    
    def _continue_turn(self):
        if not hasattr(self, 'target_x'):
            return
        
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx**2 + dy**2)**0.5
        
        if dist < 3:
            self.turning = False
            self.lane = self.destination
            if self.destination.startswith('A'):
                self.horizontal, self.direction = False, 1
            elif self.destination.startswith('B'):
                self.horizontal, self.direction = False, -1
            elif self.destination.startswith('C'):
                self.horizontal, self.direction = True, -1
            else:
                self.horizontal, self.direction = True, 1
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
    
    def is_off_screen(self):
        return self.x < -100 or self.x > WIDTH + 100 or self.y < -100 or self.y > HEIGHT + 100
    
    def draw(self):
        if self.road == "A":
            img = pygame.transform.rotate(car_img, 0)
        elif self.road == "B":
            img = pygame.transform.rotate(car_img, 180)
        elif self.road == "C":
            img = pygame.transform.rotate(car_img, 90)
        else:
            img = pygame.transform.rotate(car_img, 270)
        screen.blit(img, (int(self.x), int(self.y)))


class TrafficSimulator:
    def __init__(self):
        self.socket_client = SocketClient()
        self.running = False
        self.traffic_data = None
        self.cars = {}  # Dict: vehicle_id -> Car
        self.light_states = {"A": "red", "B": "red", "C": "red", "D": "red"}
    
    def update_from_data(self, data):
        if not data:
            return
        
        # Update lights
        current_green = data.get('current_green_road', None)
        for road in self.light_states:
            self.light_states[road] = "green" if road == current_green else "red"
        
        # Update cars from queue data
        queues = data.get('queues', {})
        new_cars = {}
        
        for lane, queue_data in queues.items():
            vehicles = queue_data.get('vehicles', [])
            for idx, vehicle in enumerate(vehicles):
                v_id = vehicle['id']
                if v_id in self.cars:
                    new_cars[v_id] = self.cars[v_id]
                else:
                    new_cars[v_id] = Car(vehicle, idx)
        
        self.cars = new_cars
    
    def draw(self):
        screen.blit(background, (0, 0))
        
        # Draw cars
        for car in self.cars.values():
            car.draw()
        
        # Cover lights with black
        for road, lights in light_rects.items():
            state = self.light_states.get(road, "red")
            if state == "green":
                pygame.draw.rect(screen, BLACK, lights["RED"])
            else:
                pygame.draw.rect(screen, BLACK, lights["GREEN"])
        
        pygame.display.flip()
    
    def update(self):
        # Move all cars
        for car in list(self.cars.values()):
            light_state = self.light_states.get(car.road, "red")
            car.move(light_state)
            
            # Remove off-screen cars
            if car.is_off_screen():
                del self.cars[car.id]
    
    def run(self):
        if not self.socket_client.start(self.update_from_data):
            return
        
        self.running = True
        print("\n[SIMULATOR] Running...\n")
        
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                
                self.update()
                self.draw()
                clock.tick(FPS)
                
        except KeyboardInterrupt:
            print("\n[STOPPED]")
        finally:
            self.socket_client.client.close()
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    simulator = TrafficSimulator()
    simulator.run()