class Vehicles:
    def __init__(self, V_type, spawn, home, spd, acc):
        #place of birth
        self.spawn = spawn
        #place of death
        self.home = home
        self.speed = spd
        #m/s
        self.acceleration = acc


    def move(self):
        #movement logic with respect to gui

        pass


class Car(Vehicles):
    def __init__(self,spawn, home, spd):
        super().__init__("car",spawn, home, spd)



class Bike(Vehicles):
    def __init__(self,spawn, home, spd):
        super().__init__("bike",spawn, home, spd)


class Bus(Vehicles):
    def __init__(self,spawn, home, spd):
        super().__init__("bus",spawn, home, spd)
