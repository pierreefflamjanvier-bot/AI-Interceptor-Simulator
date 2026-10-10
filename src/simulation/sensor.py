import random
import math

class Sensor:
    def __init__(self, position_noise=10,detection_range=500, field_of_view=120,visual_lock_range=100,visual_noise=2):
        self.position_noise=(position_noise)
        self.detection_range=(detection_range)
        self.field_of_view=(field_of_view)
        self.visual_lock_range=(visual_lock_range)
        self.visual_noise=(visual_noise)
        self.visual_lock=False
        self.last_angle_error=0


    def observe(self, target,interceptor):
        distance=math.sqrt((target.x-interceptor.x)**2+(target.y-interceptor.y)**2)
        target_angle= math.degrees(math.atan2(target.y-interceptor.y,target.x-interceptor.x))
        angle_error=(target_angle-interceptor.heading)
        if distance<=self.visual_lock_range:
            self.visual_lock=True
            current_noise=self.visual_noise
        else:
            self.visual_lock=False
            current_noise=self.position_noise

        while angle_error>180:
            angle_error-=360
        while angle_error<-180:
            angle_error+=360
        if abs(angle_error)>self.field_of_view/2:
            return None
        self.last_angle_error=angle_error

        if distance>self.detection_range:
            return None
        mesured_x=(target.x+random.gauss(0,current_noise))
        mesured_y=(target.y+random.gauss(0,current_noise))
        return(mesured_x,mesured_y )


