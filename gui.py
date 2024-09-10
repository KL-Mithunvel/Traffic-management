"""import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1400, 800))  # Width, Height
pygame.display.set_caption('Basic Pygame Window')

# Main game loop
running = True
background = pygame.image.load(r'images/intersection.jpg')
# Resize the background if necessary to fit the window size
background = pygame.transform.scale(background, (1400, 800))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the close button is clicked
            running = False

    # Fill the screen with a color (RGB format)
    screen.fill((0, 0, 255))  # Blue background
    screen.blit(background,(0,0))
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()"""
"""
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1400, 800))  # Width, Height
pygame.display.set_caption('Traffic Flow Simulation')

# Load the background image
background = pygame.image.load(r'images/intersection.jpg')
background = pygame.transform.scale(background, (1400, 800))

# Define the Car class
class Car:
    def __init__(self, image_path, start_pos, speed):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 80))  # Adjust size to fit road
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# List of spawn points for cars at the junction (based on your image)
spawn_points = [
    (180, 260),  # Bottom left junction
    (320, 100),  # Top middle junction
    (950, 100),  # Top right junction
    (1090, 260),  # Right middle junction
]

# List of destinations (possible end points)
end_points = [
    (950, 610),
    (1090, 450),
    (320, 260),
    (950, 260),
]

# List to store cars
cars = []

# Define car generation time and speed
CAR_GENERATION_INTERVAL = 2000  # Generate a car every 2 seconds
car_spawn_timer = 0
car_speed = 2

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))  # Draw the background
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate new cars at intervals
    if current_time - car_spawn_timer > CAR_GENERATION_INTERVAL:
        car_spawn_timer = current_time
        start_pos = random.choice(spawn_points)
        new_car = Car('images/up/car.png', start_pos, car_speed)  # Use any car image path
        cars.append(new_car)

    # Move and draw each car
    for car in cars:
        car.move()
        car.draw(screen)

    pygame.display.update()
    clock.tick(60)  # 60 FPS

pygame.quit()
"""

import pygame
import csv
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Define road paths (waypoints)
# Define your road paths here (customize as per the image)
road_1 = [(100, 100), (100, 200), (100, 300), (100, 400), (100, 500)]  # Vertical road
road_2 = [(150, 200), (250, 200), (350, 200), (450, 200)]  # Horizontal road


# Add more roads if needed

# Car class
class Car:
    def _init_(self, path, speed, start_time):
        self.path = path
        self.speed = speed
        self.start_time = start_time
        self.current_point_index = 0  # Start at the first point in the path
        self.image = pygame.image.load(r'path_to_your_car_image.png')  # Load your car image
        self.image = pygame.transform.scale(self.image, (40, 20))  # Resize the car image
        self.x, self.y = self.path[self.current_point_index]

    def update(self, current_time):
        if current_time >= self.start_time and self.current_point_index < len(self.path) - 1:
            target_x, target_y = self.path[self.current_point_index + 1]

            # Move towards the next waypoint
            if self.x < target_x:
                self.x += self.speed
            elif self.x > target_x:
                self.x -= self.speed

            if self.y < target_y:
                self.y += self.speed
            elif self.y > target_y:
                self.y -= self.speed

            # If the car reaches the next point, move to the next point
            if abs(self.x - target_x) < self.speed and abs(self.y - target_y) < self.speed:
                self.current_point_index += 1


# Function to load cars from CSV
def load_cars_from_csv(file_path):
    cars = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            car_id = int(row['car_id'])
            path_name = row['path']  # Fetch the path name (road_1, road_2, etc.)
            speed = int(row['speed'])
            start_time = float(row['start_time'])
            # Assign the path based on the CSV input
            path = eval(path_name)
            cars.append(Car(path, speed, start_time))
    return cars


# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Car Movement Simulation')

# Load the road layout image (background)
background = pygame.image.load(r"/mnt/data/image.png")  # Use the road layout image provided
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load car data from CSV
cars = load_cars_from_csv(r"path_to_your_cars.csv")  # Replace with actual CSV file path

# Set up the clock
clock = pygame.time.Clock()

# Main loop
running = True
start_simulation_time = time.time()
while running:
    current_time = time.time() - start_simulation_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the car positions
    for car in cars:
        car.update(current_time)

    # Draw the background (road layout)
    screen.blit(background, (0, 0))

    # Draw the cars
    for car in cars:
        screen.blit(car.image, (car.x, car.y))

    # Update the display
    pygame.display.flip()

    # Frame rate control
    clock.tick(FPS)

# Quit Pygame
pygame.quit()

