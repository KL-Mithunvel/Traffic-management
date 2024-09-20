import random
import time
import threading
import pygame
import sys
import csv
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
     # Initialize an empty list to store rows
    table = []
    
    # Read each row and append it to the list
    for row in reader:
        table.append([float(value) for value in row])

# Assigning values to 16 different variables from the first 4 rows of the CSV
a1, a2, a3, a4 = table[0]
b1, b2, b3, b4 = table[1]
c1, c2, c3, c4 = table[2]

defaultGreen = {0: int(round(float(a1))), 1: int(round(float(a2))), 2: int(round(float(a3))), 3: int(round(float(a4)))}
defaultRed = 150
defaultYellow = 5

defaultGreen2 = {0:int(round(float(b1))), 1:int(round(float(b2))), 2:int(round(float(b3))), 3:int(round(float(b4)))}
defaultRed2 = 150
defaultYellow2 = 5


defaultGreen3 = {0:int(round(float(c1))), 1:int(round(float(c2))), 2:int(round(float(c3))), 3:int(round(float(c4)))}
defaultRed3 = 150
defaultYellow3 = 5

signals = []
noOfSignals = 4
currentGreen = 0 # Indicates which signal is green currently
nextGreen = (currentGreen+1)%noOfSignals # Indicates which signal will turn green next
currentYellow = 0 # Indicates whether yellow signal is on or off 

signals2 = []
noOfSignals2 = 4
currentGreen2 = 0   # Indicates which signal is green currently
nextGreen2 = (currentGreen2+1)%noOfSignals2    # Indicates which signal will turn green next
currentYellow2 = 0   # Indicates whether yellow signal is on or off 


signals3 = []
noOfSignals3 = 4
currentGreen3 = 0   # Indicates which signal is green currently
nextGreen3 = (currentGreen3+1)%noOfSignals3    # Indicates which signal will turn green next
currentYellow3 = 0   # Indicates whether yellow signal is on or off 

speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'bike':2.5} # average speeds of vehicles

# Coordinates of vehicles' start
x = {'right':[0, 0, 0], 'down':[300, 285, 265], 'left':[1400, 1400, 1400], 'up':[212, 219, 239], 'down1' : [1070, 1055, 1035],  'up1': [577, 584, 604], 'up2': [979, 986, 1006],'left1':[1400, 1400, 1400]}
y = {'right':[158, 170, 190], 'down':[0, 0, 0], 'left':[258, 238, 218], 'up':[800, 800, 800], 'down1':[0, 0, 0], 'up1':[800, 800, 800], 'up2':[800, 800, 800],'left1':[608, 588, 568]}
# Add new directions and coordinates




vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}, 'down1': {0:[], 1:[], 2:[], 'crossed':0}, 'left1': {0:[], 1:[], 2:[], 'crossed':0}, 'up1': {0:[], 1:[], 2:[], 'crossed':0},'up2': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up', 4: 'up1' , 5: 'up2' , 6: 'down1' , 7:'left1'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(180,100),(320,100),(320,260),(180,260)]
signalTimerCoods = [(160,100),(300,100),(300,260),(160,260)]

signalCoods2 = [(950,100),(1090,100),(1090,260),(950,260)]
signalTimerCoods2 = [(930,100),(1070,100),(1070,260),(930,260)]

signalCoods3 = [(950,450),(1090,450),(1090,610),(950,610)]
signalTimerCoods3 = [(930,450),(1070,450),(1070,610),(930,610)]

# Coordinates of stop lines
stopLines = {'right': 210, 'down': 170, 'left': 300, 'up': 247, 'down1' : 170,  'up1':580 , 'up2': 590,'left1': 1080}
defaultStop = {'right': 200, 'down': 160, 'left': 310, 'up': 257, 'down1' : 160,  'up1':600 , 'up2': 610,'left1': 1090}


stoppingGap = 15 # stopping gap
movingGap = 15 # moving gap

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""
 
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.has_turned = False
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)

        if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0): 
            if(direction=='right'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().width 
                - stoppingGap 
            elif(direction=='left'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().width 
                + stoppingGap
            elif(direction=='down'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().height 
                - stoppingGap
            elif(direction=='up'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().height 
                + stoppingGap
            elif(direction=='up1'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().height 
                + stoppingGap
            elif(direction=='up2'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().height 
                + stoppingGap
            elif(direction=='down1'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().height 
                - stoppingGap
            elif(direction=='left1'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().width 
                + stoppingGap
        else:
            self.stop = defaultStop[direction]
        
        # Set new starting and stopping coordinate
        if(direction=='right'):
            temp = self.image.get_rect().width + stoppingGap 
            x[direction][lane] -= temp
        elif(direction=='left'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif(direction=='down'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif(direction=='up'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        elif(direction=='up1'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        elif(direction=='up2'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        elif(direction=='down1'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif(direction=='left1'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.image.get_rect().width>stopLines[self.direction]):   
                self.crossed = 1
            if((self.x+self.image.get_rect().width<=self.stop or self.crossed == 1 or (currentGreen==0 and currentYellow==0)) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap))):                
                self.x += self.speed 
        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
            if((self.y+self.image.get_rect().height<=self.stop or self.crossed == 1 or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap))):                
                self.y += self.speed
        elif(self.direction=='left'):
            if(self.crossed==0 and self.x<stopLines[self.direction]):
                self.crossed = 1
            if((self.x>=self.stop or self.crossed == 1 or (currentGreen==2 and currentYellow==0)) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):                
                self.x -= self.speed   
        elif(self.direction=='up'):
            if(self.crossed==0 and self.y<stopLines[self.direction]):
                self.crossed = 1
            if((self.y>=self.stop or self.crossed == 1 or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):                
                self.y -= self.speed
        elif(self.direction=='up1'):
                # Move the vehicle upwards until it reaches the rotate_y point
            if self.crossed == 0 and self.y < stopLines[self.direction]:
                self.crossed = 1
            if self.y <= 535:  # rotate_y is the Y-coordinate where the vehicle turns
        # Check if the vehicle has already turned
                if not self.has_turned:
            # Rotate the vehicle by 90 degrees to the right
                    self.image = pygame.transform.rotate(self.image, -90)  # Rotate 90 degrees to the right
                    self.has_turned = True  # Mark the vehicle as turned
                # Removed the signal check logic, so the vehicle moves regardless of signal status
        # Now move the vehicle to the right (positive X direction)
                if (self.index == 0):
                    self.x += self.speed  # Move to the right

            else:
                # Move the vehicle upwards if it's still before the turning point
                if (self.index == 0 ):
                    self.y -= self.speed  # Move upwards

        elif(self.direction=='up2'):
            if(self.crossed==0 and self.y<stopLines[self.direction]):
                self.crossed = 1
            if((self.y>=self.stop or self.crossed == 1 or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):                
                self.y -= self.speed
        elif(self.direction=='down1'):
            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
            if((self.y+self.image.get_rect().height<=self.stop or self.crossed == 1 or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap))):                
                self.y += self.speed
        elif self.direction == 'left1':
            if self.crossed == 0 and self.x < stopLines[self.direction]:
                self.crossed = 1

            # Move the vehicle along the x-axis (left) until it reaches the turning point (x <= 635)
            if (self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (
                self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][self.index - 1].image.get_rect().width + movingGap)):
                
                # Check if the vehicle has reached the turning point
                if self.x <= 635:
                    # Turn the vehicle if it has not already turned
                    if not self.has_turned:
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.has_turned = True  # Mark as turned

                    # After turning, move the vehicle upwards (y-axis only)
                    if self.index == 0 or (self.y > (vehicles[self.direction][self.lane][self.index].y + vehicles[self.direction][self.lane][self.index].image.get_rect().height + movingGap)):
                        self.y += self.speed  # Move upwards (y-axis)
                
                else:
                    # Before turning, move the vehicle left (x-axis)
                    if self.index == 0 or (self.x > (vehicles[self.direction][self.lane][self.index].x + vehicles[self.direction][self.lane][self.index].image.get_rect().width + movingGap)):
                        self.x -= self.speed

# Initialization of signals with default values
def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
    signals.append(ts4)
    repeat()

def initialize2():
    ts1 = TrafficSignal(0, defaultYellow2, defaultGreen2[0])
    signals2.append(ts1)
    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow2, defaultGreen2[1])
    signals2.append(ts2)
    ts3 = TrafficSignal(defaultRed2, defaultYellow2, defaultGreen2[2])
    signals2.append(ts3)
    ts4 = TrafficSignal(defaultRed2, defaultYellow2, defaultGreen2[3])
    signals2.append(ts4)
    repeat2()

def initialize3():
    ts1 = TrafficSignal(0, defaultYellow3, defaultGreen3[0])
    signals3.append(ts1)
    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow3, defaultGreen3[1])
    signals3.append(ts2)
    ts3 = TrafficSignal(defaultRed3, defaultYellow3, defaultGreen3[2])
    signals3.append(ts3)
    ts4 = TrafficSignal(defaultRed3, defaultYellow3, defaultGreen3[3])
    signals3.append(ts4)
    repeat3()


def repeat():
    global currentGreen, currentYellow, nextGreen
    while(signals[currentGreen].green>0):   # while the timer of current green signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 1   # set yellow signal on
    # reset stop coordinates of lanes and vehicles 
    for i in range(0,3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
    while(signals[currentGreen].yellow>0):  # while the timer of current yellow signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 0   # set yellow signal off
    
     # reset all signal times of current signal to default times
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed
       
    currentGreen = nextGreen # set next signal as green signal
    nextGreen = (currentGreen+1)%noOfSignals    # set next green signal
    signals[nextGreen].red = signals[currentGreen].yellow+signals[currentGreen].green    # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat()   

def repeat2():
    global currentGreen2, currentYellow2, nextGreen2
    while(signals2[currentGreen2].green>0):   # while the timer of current green signal is not zero
        updateValues2()
        time.sleep(1)
    currentYellow2 = 1   # set yellow signal on
    # reset stop coordinates of lanes and vehicles 
    for i in range(0,3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
    while(signals2[currentGreen2].yellow>0):  # while the timer of current yellow signal is not zero
        updateValues2()
        time.sleep(1)
    currentYellow2 = 0   # set yellow signal off
    
    # reset all signal times of current signal to default times
    signals2[currentGreen2].green = defaultGreen2[currentGreen2]
    signals2[currentGreen2].yellow = defaultYellow2
    signals2[currentGreen2].red = defaultRed2
       
    currentGreen2 = nextGreen2  # set next signal as green signal
    nextGreen2 = (currentGreen2+1)%noOfSignals2    # set next green signal
    signals2[nextGreen2].red = signals2[currentGreen2].yellow+signals2[currentGreen2].green    # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat2()  

def repeat3():
    global currentGreen3, currentYellow3, nextGreen3
    while(signals3[currentGreen3].green>0):   # while the timer of current green signal is not zero
        updateValues3()
        time.sleep(1)
    currentYellow3 = 1   # set yellow signal on
    # reset stop coordinates of lanes and vehicles 
    for i in range(0,3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
    while(signals3[currentGreen3].yellow>0):  # while the timer of current yellow signal is not zero
        updateValues3()
        time.sleep(1)
    currentYellow3 = 0   # set yellow signal off
    
    # reset all signal times of current signal to default times
    signals3[currentGreen3].green = defaultGreen3[currentGreen3]
    signals3[currentGreen3].yellow = defaultYellow3
    signals3[currentGreen3].red = defaultRed3
       
    currentGreen3 = nextGreen3  # set next signal as green signal
    nextGreen3 = (currentGreen3+1)%noOfSignals3    # set next green signal
    signals3[nextGreen3].red = signals3[currentGreen3].yellow+signals3[currentGreen3].green    # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat3()  


# Update values of the signal timers after every second
def updateValues():
    for i in range(0, noOfSignals):
        if(i==currentGreen):
            if(currentYellow==0):
                signals[i].green-=1
            else:
                signals[i].yellow-=1
        else:
            signals[i].red-=1

def updateValues2():
    for i in range(0, noOfSignals2):
        if(i==currentGreen2):
            if(currentYellow2==0):
                signals2[i].green-=1
            else:
                signals2[i].yellow-=1
        else:
            signals2[i].red-=1

def updateValues3():
    for i in range(0, noOfSignals3):
        if(i==currentGreen3):
            if(currentYellow3==0):
                signals3[i].green-=1
            else:
                signals3[i].yellow-=1
        else:
            signals3[i].red-=1

# Generating vehicles in the simulation
def generateVehicles():
    while(True):
        vehicle_type = random.randint(0,3)
        lane_number = random.randint(1,2)
        temp = random.randint(0,199)
        direction_number = 0
        dist = [25,50,75,100,125,150,175,200]
        if(temp<dist[0]):
            direction_number = 0
        elif(temp<dist[1]):
            direction_number = 1
        elif(temp<dist[2]):
            direction_number = 2
        elif(temp<dist[3]):
            direction_number = 3
        elif(temp<dist[4]):
            direction_number = 4
        elif(temp<dist[5]):
            direction_number = 5
        elif(temp<dist[6]):
            direction_number = 6
        elif(temp<dist[7]):
            direction_number = 7
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(1)

class Main:
    thread1 = threading.Thread(name="initialization",target=initialize, args=())    # initialization
    thread1.daemon = True
    thread1.start()


    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize 
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    # New width and height for the background image
    new_width = 1400 # Adjust the width as per your requirement
    new_height = 800 # Adjust the height as per your requirement

    # Load the image and scale it to new dimensions
    background = pygame.image.load('images/intersection.png')
    background = pygame.transform.scale(background, (new_width, new_height))

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles",target=generateVehicles, args=()) # Generating vehicles
    thread2.daemon = True
    thread2.start()

    thread4 = threading.Thread(name="initialization2",target=initialize2, args=())  
    thread4.daemon = True
    thread4.start()
    
    thread3 = threading.Thread(name="initialization3",target=initialize3, args=())  
    thread3.daemon = True
    thread3.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))   # display background in simulation
        for i in range(0,noOfSignals):  # display signal and set timer according to current status: green, yello, or red
            if(i==currentGreen):
                if(currentYellow==1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                signals[i].signalText = "---"  # Always set red signal text to '---'
                screen.blit(redSignal, signalCoods[i])
        signalTexts = ["","","",""]

        #if i < len(signals):
        #    screen.blit(redSignal, signalCoods[i])

        for i in range(0,noOfSignals2):  # display signal and set timer according to current status: green, yello, or red
            if(i==currentGreen2):
                if(currentYellow2==1):
                    signals2[i].signalText = signals2[i].yellow
                    screen.blit(yellowSignal, signalCoods2[i])
                else:
                    signals2[i].signalText = signals2[i].green
                    screen.blit(greenSignal, signalCoods2[i])
            else:
                signals2[i].signalText = "---"  # Always set red signal text to '---'
                screen.blit(redSignal, signalCoods2[i])
        signalTexts = ["","","",""]

       # if i < len(signals2):
        #    screen.blit(redSignal, signalCoods2[i])


        for i in range(0,noOfSignals3):  # display signal and set timer according to current status: green, yello, or red
            if(i==currentGreen3):
                if(currentYellow3==1):
                    signals3[i].signalText = signals3[i].yellow
                    screen.blit(yellowSignal, signalCoods3[i])
                else:
                    signals3[i].signalText = signals3[i].green
                    screen.blit(greenSignal, signalCoods3[i])
            else:
                signals3[i].signalText = "---"  # Always set red signal text to '---'
                screen.blit(redSignal, signalCoods3[i])
        signalTexts = ["","","",""]

       # if i < len(signals3):
        #  screen.blit(redSignal, signalCoods3[i])

        # display signal timer
        for i in range(0,noOfSignals):  
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods[i])

        for i in range(0,noOfSignals2):  
            signalTexts[i] = font.render(str(signals2[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods2[i])
        
        for i in range(0,noOfSignals3):  
            signalTexts[i] = font.render(str(signals3[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods3[i])


        # display the vehicles
        for vehicle in simulation:  
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()
        pygame.display.update()


Main()
