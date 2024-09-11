import pygame
import sys
import time
import csv

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Load background image (path should be adjusted if necessary)
background = pygame.image.load("images/intersection.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock for frame rate control
clock = pygame.time.Clock()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vehicle Simulation with CSV-based Traffic Lights")

# Define traffic light class
class TrafficLight(pygame.sprite.Sprite):
    def __init__(self, position, green_time, red_time):
        super().__init__()
        self.green_time = green_time
        self.red_time = red_time
        self.image = pygame.Surface([20, 60])
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.state = "green"  # Initial state
        self.last_switch = time.time()

    def update(self):
        # Switch between red and green based on timings
        current_time = time.time()
        if self.state == "green" and current_time - self.last_switch > self.green_time:
            self.state = "red"
            self.last_switch = current_time
        elif self.state == "red" and current_time - self.last_switch > self.red_time:
            self.state = "green"
            self.last_switch = current_time

        # Update the light color
        if self.state == "green":
            self.image.fill(GREEN)
        else:
            self.image.fill(RED)



# Define vehicle class
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed, path, traffic_lights):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.path = path
        self.path_index = 0  # Track position along the path
        self.rect.center = self.path[self.path_index]  # Start position on the path
        self.traffic_lights = traffic_lights

    def update(self):
        if self.path_index < len(self.path) - 1:
            # Get the next target point
            target_x, target_y = self.path[self.path_index]

            # Check if near any traffic light and if red, stop
            for light in self.traffic_lights:
                if self.rect.colliderect(light.rect):
                    if light.state == "red":
                        return  # Stop at red light

            # Move towards the target point
            direction_x = target_x - self.rect.centerx
            direction_y = target_y - self.rect.centery
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

            # Move by speed towards the next point
            if distance > self.speed:
                self.rect.centerx += self.speed * (direction_x / distance)
                self.rect.centery += self.speed * (direction_y / distance)
            else:
                self.path_index += 1

# Function to load timings from CSV
def load_timings(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header if present
        for row in reader:
            try:
                green_time = float(row[0])  # Use float instead of int
                red_time = float(row[1])    # Use float instead of int
                return green_time, red_time
            except ValueError as e:
                print(f"ValueError: {e} - Row contents: {row}")
                raise



# Traffic light positions (you can adjust based on the image)
junction_positions = [(320, 240), (640, 360), (960, 480)]

# Load traffic light timings from CSV files
green_time_1, red_time_1 = load_timings(r"C:\Users\klmit\OneDrive - Sree Murugan Tile Works\Desktop\hughjass.csv")
green_time_2, red_time_2 = load_timings(r"C:\Users\klmit\OneDrive - Sree Murugan Tile Works\Desktop\hughjass.csv")
green_time_3, red_time_3 = load_timings(r"C:\Users\klmit\OneDrive - Sree Murugan Tile Works\Desktop\hughjass.csv")

# Create traffic lights
traffic_light_1 = TrafficLight(junction_positions[0], green_time_1, red_time_1)
traffic_light_2 = TrafficLight(junction_positions[1], green_time_2, red_time_2)
traffic_light_3 = TrafficLight(junction_positions[2], green_time_3, red_time_3)

# Group for traffic lights
traffic_lights = pygame.sprite.Group()
traffic_lights.add(traffic_light_1, traffic_light_2, traffic_light_3)

# Vehicle paths (sample paths)
vehicle_paths = [
    [(100, 100), (200, 100), (300, 100), (320, 240), (500, 240)],  # Vehicle 1 path
    [(400, 600), (640, 360), (800, 360)],  # Vehicle 2 path
    [(600, 200), (960, 480), (1100, 480)]  # Vehicle 3 path
]

# Create vehicles
vehicles = pygame.sprite.Group()
vehicles.add(Vehicle(BLUE, 20, 10, 2, vehicle_paths[0], traffic_lights))
vehicles.add(Vehicle(RED, 20, 10, 2, vehicle_paths[1], traffic_lights))
vehicles.add(Vehicle(GREEN, 20, 10, 2, vehicle_paths[2], traffic_lights))

# Main simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update traffic lights and vehicles
    traffic_lights.update()
    vehicles.update()

    # Draw everything
    screen.blit(background, (0, 0))
    traffic_lights.draw(screen)
    vehicles.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
