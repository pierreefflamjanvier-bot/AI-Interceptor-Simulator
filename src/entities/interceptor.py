import math
class Interceptor:
    def __init__(self, x, y,  speed, strategy, heading, max_turn_rate,max_acceleration):
        self.x = x
        self.y = y
        self.speed = speed
        self.strategy = strategy
        self.history=[]
        self.finished= False
        self.interception_time=None
        self.heading=heading
        self.max_turn_rate=max_turn_rate
        self.max_acceleration=max_acceleration
        self.current_speed=0 
         

    def update(self, dt, track):

        desired_heading=(self.strategy.compute_direction(self, track))
        heading_error=(desired_heading-self.heading)

        while heading_error>180:
            heading_error-=360
        while heading_error<-180:
            heading_error+=360

        max_turn=self.max_turn_rate*dt
        heading_change=max(-max_turn,min(max_turn,heading_error))
        self.heading+=heading_change
        self.heading%=360
        
        target_speed=self.speed
        self.current_speed+=(self.max_acceleration*dt)
        if self.current_speed>target_speed:
            self.current_speed=target_speed

        vx=(self.current_speed*math.cos(math.radians(self.heading)))
        vy=(self.current_speed*math.sin(math.radians(self.heading)))
        self.x+=vx*dt
        self.y+=vy*dt
        self.history.append((self.x, self.y))

    