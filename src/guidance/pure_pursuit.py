import math
from guidance.base_strategy import GuidanceStrategy

class PurePursuit(GuidanceStrategy):

    def compute_direction(self, interceptor, target):

        dx=target.x-interceptor.x
        dy=target.y-interceptor.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance==0:
            return 0, 0

        return dx/distance,dy/distance