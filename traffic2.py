import random
import threading
import time
import sys
import pygame

# Define global variables
signals = []
vehicles = {0: [], 1: [], 2: [], 3: []}  # List for vehicles in each direction
currentGreen = 0
currentYellow = 0
nextGreen = 1
noOfSignals = 4
randomGreenSignalTimer = True
randomGreenSignalTimerRange = [10, 20]
defaultGreen = [10, 15, 20, 25]
defaultYellow = 5
defaultRed = 40
allowedVehicleTypes = {'car': True, 'bus': True, 'bike': True, 'truck': True}
allowedVehicleTypesList = []
directionNumbers = [0, 1, 2, 3]
signalCoods = [(300, 200), (400, 200), (500, 200), (600, 200)]
signalTimerCoods = [(300, 250), (400, 250), (500, 250), (600, 250)]
defaultStop = [250, 350, 450, 550]


# Class definitions
class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = "---"


class Vehicle:
    def __init__(self, lane, vehicle_type, direction_number, direction, will_turn):
        self.lane = lane
        self.vehicle_type = vehicle_type
        self.direction_number = direction_number
        self.direction = direction
        self.will_turn = will_turn
        self.image = pygame.image.load("images/" + vehicle_type + ".png")  # Load vehicle image
        self.x, self.y = 100, defaultStop[direction_number]  # Initial position

    def move(self):
        # Move vehicle logic here; adjust position based on direction and lane
        self.x += 1  # Example: Move vehicle horizontally


# Initialization of signals with default values
def initialize():
    minTime = randomGreenSignalTimerRange[0]
    maxTime = randomGreenSignalTimerRange[1]

    if randomGreenSignalTimer:
        ts1 = TrafficSignal(0, defaultYellow, random.randint(minTime, maxTime))
        signals.append(ts1)
        ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, random.randint(minTime, maxTime))
        signals.append(ts2)
        ts3 = TrafficSignal(defaultRed, defaultYellow, random.randint(minTime, maxTime))
        signals.append(ts3)
        ts4 = TrafficSignal(defaultRed, defaultYellow, random.randint(minTime, maxTime))
        signals.append(ts4)
    else:
        ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
        signals.append(ts1)
        ts2 = TrafficSignal(ts1.yellow + ts1.green, defaultYellow, defaultGreen[1])
        signals.append(ts2)
        ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
        signals.append(ts3)
        ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
        signals.append(ts4)

    repeat()


def repeat():
    global currentGreen, currentYellow, nextGreen
    while signals[currentGreen].green > 0:
        updateValues()
        time.sleep(1)

    currentYellow = 1
    for vehicle in vehicles[directionNumbers[currentGreen]]:
        vehicle.stop = defaultStop[directionNumbers[currentGreen]]

    while signals[currentGreen].yellow > 0:
        updateValues()
        time.sleep(1)

    currentYellow = 0

    # Reset all signal times
    if randomGreenSignalTimer:
        signals[currentGreen].green = random.randint(randomGreenSignalTimerRange[0], randomGreenSignalTimerRange[1])
    else:
        signals[currentGreen].green = defaultGreen[currentGreen]

    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen
    nextGreen = (currentGreen + 1) % noOfSignals
    signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green
    repeat()


# Update values of the signal timers after every second
def updateValues():
    for i in range(noOfSignals):
        if i == currentGreen:
            if currentYellow == 0:
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


# Generating vehicles in the simulation
def generateVehicles():
    while True:
        vehicle_type = random.choice(allowedVehicleTypesList)

        lane_number = 1  # Only one lane now

        will_turn = 0
        temp = random.randint(0, 99)
        if temp < 40:
            will_turn = 1

        temp = random.randint(0, 99)
        direction_number = 0
        dist = [25, 50, 75, 100]
        if temp < dist[0]:
            direction_number = 0
        elif temp < dist[1]:
            direction_number = 1
        elif temp < dist[2]:
            direction_number = 2
        elif temp < dist[3]:
            direction_number = 3

        vehicle = Vehicle(lane_number, vehicle_type, direction_number, directionNumbers[direction_number], will_turn)
        vehicles[direction_number].append(vehicle)  # Add vehicle to the list of the correct direction
        time.sleep(1)


class Main:
    global allowedVehicleTypesList
    i = 0
    for vehicleType in allowedVehicleTypes:
        if allowedVehicleTypes[vehicleType]:
            allowedVehicleTypesList.append(vehicleType)

    thread1 = threading.Thread(name="initialization", target=initialize)
    thread1.daemon = True
    thread1.start()

    # Pygame setup
    pygame.init()

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Background image
    new_width = 1400
    new_height = 800
    background = pygame.image.load('images/intersection.png')
    background = pygame.transform.scale(background, (new_width, new_height))

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles)
    thread2.daemon = True
    thread2.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))  # Display background
        for i in range(noOfSignals):  # Display signal and set timer
            if i == currentGreen:
                if currentYellow == 1:
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if signals[i].red <= 10:
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])

        signalTexts = ["", "", "", ""]
        for i in range(noOfSignals):
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods[i])

        # Display the vehicles
        for direction in vehicles:
            for vehicle in vehicles[direction]:
                screen.blit(vehicle.image, [vehicle.x, vehicle.y])
                vehicle.move()

        pygame.display.update()


Main()
