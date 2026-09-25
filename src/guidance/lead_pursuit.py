#Dans l'algorythme de lead pursuit, l'intercepteur ne se dirige pas vers la position actuelle de la cible, mais vers un point anticipé de sa trajectoire. Cela permet d'éviter les trajectoires en zigzag et d'améliorer l'efficacité de l'interception.

import math

from entities import interceptor, target
from guidance.base_strategy import GuidanceStrategy


class LeadPursuit(GuidanceStrategy):

    def compute_direction(self,interceptor,track):

        distance = math.sqrt((track.x - interceptor.x)**2+(track.y - interceptor.y)**2)

        prediction_time = (distance/interceptor.speed)

        future_x = (track.x+track.vx * prediction_time)

        future_y = (track.y+track.vy * prediction_time)

        dx = future_x - interceptor.x
        dy = future_y - interceptor.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return 0, 0

        return (dx / distance,dy / distance)