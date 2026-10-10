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
        self.predicted=False
        self.time_since_measurement=0
        self.max_prediction_time=5
        self.confidence=100
        self.confidence_decay_rate=25
        self.confidence_recovery_rate=50

    def update(self,measurment,dt):
        old_x=self.x
        old_y=self.y
        if measurment is None:
            self.confidence-=self.confidence_decay_rate*dt
            if self.confidence<0:
                self.confidence=0
                self.valid=False
                return
            drag=0.98
            self.vx*=drag
            self.vy*=drag
            self.x+=self.vx*dt
            self.y+=self.vy*dt
            self.valid=True
            self.predicted=True
            self.time_since_measurement+=dt
            if(self.time_since_measurement>self.max_prediction_time):
                self.valid=False
            return
        self.time_since_measurement=0
        self.valid=True
        self.predicted=False
        self.confidence=min(100,self.confidence+self.confidence_recovery_rate*dt)
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

        MAX_TRACK_SPEED=300
        speed=math.sqrt(self.vx**2+self.vy**2)
        if speed>MAX_TRACK_SPEED:
            fatcor=MAX_TRACK_SPEED/speed
            self.vx*=fatcor
            self.vy*=fatcor

        self.heading=math.degrees(math.atan2(self.vy,self.vx))