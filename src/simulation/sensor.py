import random

class Sensor:
    def __init__(self, position_noise=5):
        self.position_noise=(position_noise)

    def observe(self, target):
        mesured_x=(target.x+random.gauss(0,self.position_noise))
        mesured_y=(target.y+random.gauss(0,self.position_noise))
        return(mesured_x,mesured_y )
