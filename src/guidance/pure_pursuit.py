#dans l'algorythme de pure poursuite, l'intercepteur se dirige toujours vers la position actuelle de la cible. Cela peut entraîner des trajectoires en zigzag si la cible change de direction fréquemment.

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