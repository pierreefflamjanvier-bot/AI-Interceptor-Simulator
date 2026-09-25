#Algorytheme de proportional Navigation, l'intercepteur ajuste sa direction en fonction de la vitesse de rotation de la ligne de visée vers la cible. Cela permet d'anticiper les mouvements de la cible et d'améliorer l'efficacité de l'interception.

import math
from guidance.base_strategy import GuidanceStrategy
class ProportionalNavigation(GuidanceStrategy):

    def __init__(self):
        self.previous_los_angle=None
        self.N=4
    
    def compute_direction(self,interceptor,track):
        dx = track.x - interceptor.x
        dy = track.y - interceptor.y
        los_angle=math.atan2(dy,dx)
        if self.previous_los_angle is None:
            self.previous_los_angle = los_angle
            return (math.cos(los_angle),math.sin(los_angle))
        los_rate = (los_angle-self.previous_los_angle)
        self.previous_los_angle = los_angle
        commanded_angle = los_angle+self.N * los_rate
        return (math.cos(commanded_angle),math.sin(commanded_angle))
            
            