import math

from guidance.base_strategy import GuidanceStrategy


class PurePursuit(GuidanceStrategy):

    def compute_direction(
        self,
        interceptor,
        track
    ):

        dx = track.x - interceptor.x
        dy = track.y - interceptor.y

        distance = math.sqrt(
            dx**2 + dy**2
        )

        if distance == 0:
            return 0, 0
    
        desired_heading = math.degrees(math.atan2(dy, dx))
        return desired_heading
    