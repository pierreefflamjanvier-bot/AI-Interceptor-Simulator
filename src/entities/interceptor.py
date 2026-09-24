class Interceptor:
    def __init__(self, x, y,  speed, strategy):
        self.x = x
        self.y = y
        self.speed = speed
        self.strategy = strategy
        self.history=[]
         

    def update(self, dt, target):

        dx, dy=self.strategy.compute_direction(self, target)
        self.x += dx * self.speed*dt
        self.y += dy * self.speed*dt
        self.history.append((self.x, self.y))

    