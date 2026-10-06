import random
import math

class Sensor:
    def __init__(self, position_noise=10,detection_range=500):
        self.position_noise=(position_noise)
        self.detection_range=(detection_range)


    def observe(self, target,interceptor):
        distance=math.sqrt((target.x-interceptor.x)**2+(target.y-interceptor.y)**2)
        if distance>self.detection_range:
            return None
        mesured_x=(target.x+random.gauss(0,self.position_noise))
        mesured_y=(target.y+random.gauss(0,self.position_noise))
        return(mesured_x,mesured_y )
