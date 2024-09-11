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
    header = next(reader)
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

defaultGreen2 = {0: int(round(float(b1))), 1: int(round(float(b2))), 2: int(round(float(b3))), 3: int(round(float(b4)))}
defaultRed2 = 150
defaultYellow2 = 5

defaultGreen3 = {0: int(round(float(c1))), 1: int(round(float(c2))), 2: int(round(float(c3))), 3: int(round(float(c4)))}
defaultRed3 = 150
defaultYellow3 = 5

signals = []
noOfSignals = 4
currentGreen = 0  # Indicates which signal is green currently
nextGreen = (currentGreen + 1) % noOfSignals  # Indicates which signal will turn green next
currentYellow = 0  # Indicates whether yellow signal is on or off

signals2 = []
noOfSignals2 = 4
currentGreen2 = 0  # Indicates which signal is green currently
nextGreen2 = (currentGreen2 + 1) % noOfSignals2  # Indicates which signal will turn green next
currentYellow2 = 0  # Indicates whether yellow signal is on or off

signals3 = []
noOfSignals3 = 4
currentGreen3 = 0  # Indicates which signal is green currently
nextGreen3 = (currentGreen3 + 1) % noOfSignals3  # Indicates which signal will turn green next
currentYellow3 = 0  # Indicates whether yellow signal is on or off

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(180, 100), (320, 100), (320, 260), (180, 260)]
signalTimerCoods = [(160, 100), (300, 100), (300, 260), (160, 260)]

signalCoods2 = [(950, 100), (1090, 100), (1090, 260), (950, 260)]
signalTimerCoods2 = [(930, 100), (1070, 100), (1070, 260), (930, 260)]

signalCoods3 = [(950, 450), (1090, 450), (1090, 610), (950, 610)]
signalTimerCoods3 = [(930, 450), (1070, 450), (1070, 610), (930, 610)]

pygame.init()
simulation = pygame.sprite.Group()


class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""


# Initialization of signals with default values
def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
    signals.append(ts4)
    repeat()


def initialize2():
    ts1 = TrafficSignal(0, defaultYellow2, defaultGreen2[0])
    signals2.append(ts1)
    ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow2, defaultGreen2[1])
    signals2.append(ts2)
    ts3 = TrafficSignal(defaultRed2, defaultYellow2, defaultGreen2[2])
    signals2.append(ts3)
    ts4 = TrafficSignal(defaultRed2, defaultYellow2, defaultGreen2[3])
    signals2.append(ts4)
    repeat2()


def initialize3():
    ts1 = TrafficSignal(0, defaultYellow3, defaultGreen3[0])
    signals3.append(ts1)
    ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow3, defaultGreen3[1])
    signals3.append(ts2)
    ts3 = TrafficSignal(defaultRed3, defaultYellow3, defaultGreen3[2])
    signals3.append(ts3)
    ts4 = TrafficSignal(defaultRed3, defaultYellow3, defaultGreen3[3])
    signals3.append(ts4)
    repeat3()


def repeat():
    global currentGreen, currentYellow, nextGreen
    while (signals[currentGreen].green > 0):  # while the timer of current green signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 1  # set yellow signal on
    # reset stop coordinates of lanes and vehicles

    while (signals[currentGreen].yellow > 0):  # while the timer of current yellow signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 0  # set yellow signal off

    # reset all signal times of current signal to default times
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen  # set next signal as green signal
    nextGreen = (currentGreen + 1) % noOfSignals  # set next green signal
    signals[nextGreen].red = signals[currentGreen].yellow + signals[
        currentGreen].green  # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat()


def repeat2():
    global currentGreen2, currentYellow2, nextGreen2
    while (signals2[currentGreen2].green > 0):  # while the timer of current green signal is not zero
        updateValues2()
        time.sleep(1)
    currentYellow2 = 1  # set yellow signal on
    # reset stop coordinates of lanes and vehicles

    while (signals2[currentGreen2].yellow > 0):  # while the timer of current yellow signal is not zero
        updateValues2()
        time.sleep(1)
    currentYellow2 = 0  # set yellow signal off

    # reset all signal times of current signal to default times
    signals2[currentGreen2].green = defaultGreen2[currentGreen2]
    signals2[currentGreen2].yellow = defaultYellow2
    signals2[currentGreen2].red = defaultRed2

    currentGreen2 = nextGreen2  # set next signal as green signal
    nextGreen2 = (currentGreen2 + 1) % noOfSignals2  # set next green signal
    signals2[nextGreen2].red = signals2[currentGreen2].yellow + signals2[
        currentGreen2].green  # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat2()


def repeat3():
    global currentGreen3, currentYellow3, nextGreen3
    while (signals3[currentGreen3].green > 0):  # while the timer of current green signal is not zero
        updateValues3()
        time.sleep(1)
    currentYellow3 = 1  # set yellow signal on
    # reset stop coordinates of lanes and vehicles

    while (signals3[currentGreen3].yellow > 0):  # while the timer of current yellow signal is not zero
        updateValues3()
        time.sleep(1)
    currentYellow3 = 0  # set yellow signal off

    # reset all signal times of current signal to default times
    signals3[currentGreen3].green = defaultGreen3[currentGreen3]
    signals3[currentGreen3].yellow = defaultYellow3
    signals3[currentGreen3].red = defaultRed3

    currentGreen3 = nextGreen3  # set next signal as green signal
    nextGreen3 = (currentGreen3 + 1) % noOfSignals3  # set next green signal
    signals3[nextGreen3].red = signals3[currentGreen3].yellow + signals3[
        currentGreen3].green  # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat3()


# Update values of the signal timers after every second
def updateValues():
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


def updateValues2():
    for i in range(0, noOfSignals2):
        if (i == currentGreen2):
            if (currentYellow2 == 0):
                signals2[i].green -= 1
            else:
                signals2[i].yellow -= 1
        else:
            signals2[i].red -= 1


def updateValues3():
    for i in range(0, noOfSignals3):
        if (i == currentGreen3):
            if (currentYellow3 == 0):
                signals3[i].green -= 1
            else:
                signals3[i].yellow -= 1
        else:
            signals3[i].red -= 1


class Main:
    thread1 = threading.Thread(name="initialization", target=initialize, args=())  # initialization
    thread1.daemon = True
    thread1.start()

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    new_width = 1400  # Adjust the width as per your requirement
    new_height = 800  # Adjust the height as per your requirement

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

    thread2 = threading.Thread(name="initialization2", target=initialize2, args=())
    thread2.daemon = True
    thread2.start()

    thread3 = threading.Thread(name="initialization3", target=initialize3, args=())
    thread3.daemon = True
    thread3.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))  # display background in simulation

        for i in range(0,
                       noOfSignals):  # display signal and set timer according to current status: green, yello, or red
            if (i == currentGreen):
                if (currentYellow == 1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                signals[i].signalText = "---"  # Always set red signal text to '---'
                screen.blit(redSignal, signalCoods[i])
        signalTexts = ["", "", "", ""]

        if i < len(signals):
            screen.blit(redSignal, signalCoods[i])

        for i in range(0,
                       noOfSignals2):  # display signal and set timer according to current status: green, yello, or red
            if (i == currentGreen2):
                if (currentYellow2 == 1):
                    signals2[i].signalText = signals2[i].yellow
                    screen.blit(yellowSignal, signalCoods2[i])
                else:
                    signals2[i].signalText = signals2[i].green
                    screen.blit(greenSignal, signalCoods2[i])
            else:
                signals2[i].signalText = "---"  # Always set red signal text to '---'
                screen.blit(redSignal, signalCoods2[i])
        signalTexts = ["", "", "", ""]

        if i < len(signals2):
            screen.blit(redSignal, signalCoods2[i])

        for i in range(0,
                       noOfSignals3):  # display signal and set timer according to current status: green, yello, or red
            if (i == currentGreen3):
                if (currentYellow3 == 1):
                    signals3[i].signalText = signals3[i].yellow
                    screen.blit(yellowSignal, signalCoods3[i])
                else:
                    signals3[i].signalText = signals3[i].green
                    screen.blit(greenSignal, signalCoods3[i])
            else:
                signals3[i].signalText = "---"  # Always set red signal text to '---'
                screen.blit(redSignal, signalCoods3[i])
        signalTexts = ["", "", "", ""]

        if i < len(signals3):
            screen.blit(redSignal, signalCoods3[i])

        # display signal timer
        for i in range(0, noOfSignals):
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods[i])

        for i in range(0, noOfSignals2):
            signalTexts[i] = font.render(str(signals2[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods2[i])

        for i in range(0, noOfSignals3):
            signalTexts[i] = font.render(str(signals3[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods3[i])

        pygame.display.update()


Main()