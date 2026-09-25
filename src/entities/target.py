import math

class Target:
    def __init__(self, x, y, speed, heading, turn_rate):
        self.x = x
        self.y = y
        self.speed = speed
        self.heading = heading
        self.turn_rate = turn_rate

        self.history=[]

    def update(self, dt):
        self.heading += self.turn_rate * dt
        vx=self.speed * math.cos(math.radians(self.heading))
        vy=self.speed * math.sin(math.radians(self.heading))
        self.x += vx * dt
        self.y += vy * dt
        self.history.append((self.x, self.y))