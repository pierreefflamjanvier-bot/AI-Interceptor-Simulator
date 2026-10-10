import pygame
import math

from entities.target import Target
from entities.interceptor import Interceptor

from simulation.sensor import Sensor
from simulation.track import Track

from guidance.pure_pursuit import PurePursuit
from guidance.lead_pursuit import LeadPursuit
from guidance.proportional_navigation import ProportionalNavigation

from ui.debug_panel import draw_debug_panel
from ui.result_panel import draw_results_panel
from ui.trajectories import draw_trajectories
from ui.entities import draw_entities


# ==================================================
# INITIALISATION
# ==================================================

pygame.init()

SIM_WIDTH=1500
SCREEN_HEIGHT = 1000
DEBUG_WIDTH=400
SCREEN_WIDTH=SIM_WIDTH+DEBUG_WIDTH
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("AI Interceptor Simulator")

font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()


# ==================================================
# ENTITES
# ==================================================

target = Target(x=1000,y=400,speed=150,heading=180, turn_rate=-5)
interceptor_red = Interceptor(x=400,y=200,speed=200,strategy=PurePursuit(),heading=0,max_turn_rate=120,max_acceleration=220)
interceptor_blue = Interceptor(x=400,y=200,speed=200,strategy=LeadPursuit(),heading=0,max_turn_rate=120,max_acceleration=220)
interceptor_green = Interceptor(x=400,y=200,speed=200,strategy=ProportionalNavigation(),heading=0,max_turn_rate=120,max_acceleration=220)

sensor = Sensor(position_noise=30, detection_range=700, field_of_view=180,visual_lock_range=100,visual_noise=2)
track=Track()
# ==================================================
# VARIABLES
# ==================================================

running = True
elapsed_time = 0
simulation_finished = False
MAX_TIME= 60

distance_red = 0
distance_blue = 0
distance_green = 0


# ==================================================
# BOUCLE PRINCIPALE
# ==================================================

while running:
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen,(255, 255, 255),(SIM_WIDTH,0,DEBUG_WIDTH,SCREEN_HEIGHT))
    pygame.draw.line(screen,(150, 150, 150),(SIM_WIDTH,0),(SIM_WIDTH,SCREEN_HEIGHT),2)
    dt = clock.tick(60) / 1000

    # ----------------------------------------------
    # EVENEMENTS
    # ----------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # ----------------------------------------------
    # UPDATE
    # ----------------------------------------------
    if elapsed_time>MAX_TIME:
        simulation_finished=True

    if not simulation_finished:

        elapsed_time += dt

        target.update(dt)

        measurement=sensor.observe(target,interceptor_red)
        
        target_visible=(measurement is not None)
        track.update(measurement,dt)

        if not interceptor_red.finished:
            interceptor_red.update(dt, track)

        if not interceptor_blue.finished:
            interceptor_blue.update(dt, track)

        if not interceptor_green.finished:
            interceptor_green.update(dt, track)

        # ------------------------------------------
        # DISTANCES
        # ------------------------------------------

        distance_red = math.sqrt((target.x - interceptor_red.x) ** 2+(target.y - interceptor_red.y) ** 2)
        distance_blue = math.sqrt((target.x - interceptor_blue.x) ** 2+(target.y - interceptor_blue.y) ** 2)
        distance_green = math.sqrt((target.x - interceptor_green.x) ** 2+(target.y - interceptor_green.y) ** 2)

        # ------------------------------------------
        # INTERCEPTION ROUGE
        # ------------------------------------------

        if (distance_red < 10 and not interceptor_red.finished):
            interceptor_red.finished = True
            interceptor_red.interception_time = elapsed_time
            print(f"Pure Pursuit : "f"{elapsed_time:.2f} s")

        # ------------------------------------------
        # INTERCEPTION BLEU
        # ------------------------------------------

        if (distance_blue < 10 and not interceptor_blue.finished):
            interceptor_blue.finished = True
            interceptor_blue.interception_time = elapsed_time
            print(f"Lead Pursuit : "f"{elapsed_time:.2f} s")

        # ------------------------------------------
        # INTERCEPTION VERT
        # ------------------------------------------

        if (distance_green < 10 and not interceptor_green.finished):
            interceptor_green.finished = True
            interceptor_green.interception_time = elapsed_time
            print(f"Proportional Navigation : {elapsed_time:.2f} s")

        # ------------------------------------------
        # FIN DE SIMULATION
        # ------------------------------------------

        if (interceptor_red.finished and interceptor_blue.finished and interceptor_green.finished):
            simulation_finished = True

# ----------------------------------------------
# AFFICHAGE
# ----------------------------------------------

    screen.fill((255, 255, 255))

    # ----------------------------------------------
    # TRAJECTOIRES
    # ----------------------------------------------
    draw_trajectories(screen, target,interceptor_red,interceptor_blue,interceptor_green)
    # ----------------------------------------------
    # ENTITES
    # ----------------------------------------------
    draw_entities(screen,target,interceptor_red,interceptor_blue,interceptor_green,measurement,track,target_visible) 
    # ----------------------------------------------
    # CHRONO
    # ----------------------------------------------

    timer_text = font.render(f"Temps : {elapsed_time:.2f} s",True,(0, 0, 0))
    screen.blit(timer_text,(20, 20))


    # ----------------------------------------------
    # HUD
    # ----------------------------------------------

    DEBUG_X=SIM_WIDTH+20
    draw_debug_panel(screen,font,DEBUG_X,sensor,track,interceptor_red,interceptor_blue,interceptor_green,target_visible)
    draw_results_panel(screen,font,DEBUG_X,interceptor_red, interceptor_blue,interceptor_green, simulation_finished)
    
    pygame.display.flip()

pygame.quit()