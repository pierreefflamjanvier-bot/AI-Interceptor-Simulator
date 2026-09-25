import math

class Track:

    def __init__(self):
        self.x=0
        self.y=0
        self.vx=0
        self.vy=0
        self.Initialized=False

    def update(self,measurment):
        old_x=self.x
        old_y=self.y
        if not self.Initialized:
            self.x=measurment[0]
            self.y=measurment[1]
            self.Initialized=True
            return
        alpha=0.2
        self.x=alpha*measurment[0]+(1-alpha)*self.x
        self.y=alpha*measurment[1]+(1-alpha)*self.y
        self.vx=(self.x-old_x)
        self.vy=(self.y-old_y)