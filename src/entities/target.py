class Target:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.history=[]

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.history.append((self.x, self.y))