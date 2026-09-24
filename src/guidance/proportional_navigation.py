#Algorytheme de proportional Navigation, l'intercepteur ajuste sa direction en fonction de la vitesse de rotation de la ligne de visée vers la cible. Cela permet d'anticiper les mouvements de la cible et d'améliorer l'efficacité de l'interception.

import math
from guidance.base_strategy import GuidanceStrategy
class ProportionalNavigation(GuidanceStrategy):

    def compute_direction(self,interceptor,target):
        dx = target.x - interceptor.x
        dy = target.y - interceptor.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return 0, 0

        # Position future plus courte
        prediction_time = (distance/interceptor.speed) * 0.5

        future_x = (target.x+ target.vx * prediction_time)
        future_y = (target.y+ target.vy * prediction_time)

        dx = future_x - interceptor.x
        dy = future_y - interceptor.y

        distance = math.sqrt(dx**2 + dy**2)
            
        if distance == 0:
            return 0, 0

        return (dx / distance,dy / distance)
            
            