import math

class Track:

    def __init__(self):
        self.x=0
        self.y=0
        self.vx=0
        self.vy=0
        self.heading=0
        self.valid= False
        self.initialized=False

    def update(self,measurment,dt):
        old_x=self.x
        old_y=self.y
        if measurment is None:
            self.valid=False
            return
        self.valid=True
        if not self.initialized:
            self.x=measurment[0]
            self.y=measurment[1]
            self.vx=0
            self.vy=0   
            self.heading=0
            self.initialized=True
            return

        alpha=0.2
        self.x=alpha*measurment[0]+(1-alpha)*self.x
        self.y=alpha*measurment[1]+(1-alpha)*self.y
        self.vx=(self.x-old_x)/dt
        self.vy=(self.y-old_y)/dt

        self.heading=math.degrees(math.atan2(self.vy,self.vx))