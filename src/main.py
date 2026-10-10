import pygame
import math

from entities.target import Target
from entities.interceptor import Interceptor

from simulation.sensor import Sensor
from simulation.track import Track

from guidance.pure_pursuit import PurePursuit
from guidance.lead_pursuit import LeadPursuit
from guidance.proportional_navigation import ProportionalNavigation


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

sensor = Sensor(position_noise=30, detection_range=700, field_of_view=180)
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

    if len(target.history) > 1:
        pygame.draw.lines(screen,(180, 180, 180),False,target.history,2)
            
    if len(interceptor_red.history) > 1:
        pygame.draw.lines(screen,(255, 50, 50),False,interceptor_red.history,2)
            
    if len(interceptor_blue.history) > 1:
        pygame.draw.lines(screen,(0, 0, 255),False,interceptor_blue.history,2)

    if len(interceptor_green.history) > 1:
        pygame.draw.lines(screen,(0, 180, 0),False,interceptor_green.history,2) 
            
    # ----------------------------------------------
    # ENTITES
    # ----------------------------------------------

    pygame.draw.circle(screen,(0, 0, 0),(int(target.x), int(target.y)),8)
        
    pygame.draw.circle(screen,(255, 0, 0),(int(interceptor_red.x), int(interceptor_red.y)),8)
    line_length=30
    end_x=interceptor_red.x+line_length*math.cos(math.radians(interceptor_red.heading))
    end_y=interceptor_red.y+line_length*math.sin(math.radians(interceptor_red.heading)) 
    pygame.draw.line(screen,(255, 0, 0),(int(interceptor_red.x), int(interceptor_red.y)),(int(end_x), int(end_y)),2)    

    pygame.draw.circle(screen,(0, 0, 255),(int(interceptor_blue.x), int(interceptor_blue.y)),8)

    pygame.draw.circle(screen,(0, 180, 0),(int(interceptor_green.x), int(interceptor_green.y)),8)   
    if measurement is not None:
        pygame.draw.circle(screen,(255,165,0),(int(measurement[0]), int(measurement[1])),4)
    if target_visible:
        pygame.draw.circle(screen,(255,0,255),(int(track.x), int(track.y)),4)   
    # ----------------------------------------------
    # CHRONO
    # ----------------------------------------------

    timer_text = font.render(f"Temps : {elapsed_time:.2f} s",True,(0, 0, 0))
    screen.blit(timer_text,(20, 20))


    # ----------------------------------------------
    # HUD
    # ----------------------------------------------

    DEBUG_X=SIM_WIDTH+20


    #RESULTS
    result_title=font.render("-----RESULTS-----",True,(0,0,0))
    screen.blit(result_title,(DEBUG_X, 680))

    heading_red=font.render(f"Cap Rouge:{interceptor_red.heading:.1f}",True,(255,0,0))
    

    heading_blue=font.render(f"Cap Bleu:{interceptor_blue.heading:.1f}",True,(0,0,255))
    

    heading_green=font.render(f"Cap Vert:{interceptor_green.heading:.1f}",True,(0,180,0))
    

    screen.blit(font.render("Noir : Cible",True,(0, 0, 0)),(DEBUG_X-360, 10))
    screen.blit(font.render("Rouge : Pure Pursuit",True,(255, 0, 0)),(DEBUG_X-360, 50))
    screen.blit(font.render("Bleu : Lead Pursuit",True,(0, 0, 255)),(DEBUG_X-360, 90))
    screen.blit(font.render("Vert : Proportional Navigation",True,(0, 180, 0)),(DEBUG_X-360, 130)) 
    
    if target_visible:
        visibility_text=font.render("VISIBLE",True,(0,180,0))
    else:
        visibility_text=font.render("LOST",True,(255,0,0))
    

    track_text=font.render(f"Track : ({track.x:.1f},{track.y:.1f})",True,(255,0,255))
    
    track_valid_text=font.render("TRACK VALID" if track.valid else "TRACK LOST",True,(0,255,0) if track.valid else (255,0,0))


    if not track.valid:
        track_status_text="TRACK LOST"
    elif track.predicted:
        track_status_text="TRACK PREDICTED"
    else:
        track_status_text="TRACK VALID"
    track_status_surface=font.render(track_status_text,True,((255,0,0) if not track.valid else (255,165,0) if track.predicted else (0,255,0)))
    

    confidence_texte=font.render(f"Confidence:{track.confidence:.0f}%",True,(255,0,0))


    angle_text=font.render(f"Angle Error:{sensor.last_angle_error:.1f}°",True,(255,255,0))
    
    prediction_age_text=font.render(f"Prediction Age:{track.time_since_measurement:.1f}s",True,(255,255,0))
    #TITRE
    debug_title=font.render("DEBUG PANEL",True,(0,0,0))
    screen.blit(debug_title,(DEBUG_X,20))

    #SENSOR
    sensor_titel=font.render("-----SENSOR-----",True,(0,0,0))
    screen.blit(sensor_titel,(DEBUG_X, 70))
    screen.blit(visibility_text,(DEBUG_X, 110))
    screen.blit(angle_text,(DEBUG_X, 150))

    #TRACK
    track_title=font.render("-----TRACK-----",True,(0,0,0))
    screen.blit(track_title,(DEBUG_X, 220))
    screen.blit(track_status_surface,(DEBUG_X, 260))    
    screen.blit(track_text,(DEBUG_X, 300))
    screen.blit(confidence_texte,(DEBUG_X, 340))    
    screen.blit(prediction_age_text,(DEBUG_X, 380))

    #INTERCEPTORS
    interceptor_title=font.render("-----INTERCEPTORS-----",True,(0,0,0))
    screen.blit(interceptor_title,(DEBUG_X, 460))
    screen.blit(heading_red,(DEBUG_X, 510))
    screen.blit(heading_blue,(DEBUG_X, 550))
    screen.blit(heading_green,(DEBUG_X, 590))


    # ----------------------------------------------
    # RESULTATS
    # ----------------------------------------------

    if interceptor_red.interception_time is not None:
        screen.blit(font.render(f"Pure : "f"{interceptor_red.interception_time:.2f} s",True,(255, 0, 0)),(DEBUG_X, 730))

    if interceptor_blue.interception_time is not None:
        screen.blit(font.render(f"Lead : "f"{interceptor_blue.interception_time:.2f} s",True,(0, 0, 255)),(DEBUG_X, 770))

    if interceptor_green.interception_time is not None:
        screen.blit(font.render(f"Proportional : "f"{interceptor_green.interception_time:.2f} s",True,(0, 180, 0)),(DEBUG_X, 810))  

    # ----------------------------------------------
    # GAGNANT
    # ----------------------------------------------

    if simulation_finished:

        winner = "EGALITE"

        if (interceptor_red.interception_time<interceptor_blue.interception_time and interceptor_red.interception_time<interceptor_green.interception_time):
            winner = "PURE PURSUIT"

        elif (interceptor_blue.interception_time<interceptor_red.interception_time and interceptor_blue.interception_time<interceptor_green.interception_time):
            winner = "LEAD PURSUIT"

        elif (interceptor_green.interception_time<interceptor_red.interception_time and interceptor_green.interception_time<interceptor_blue.interception_time):
            winner = "PROPORTIONAL NAVIGATION"

        winner_text = font.render(f"Gagnant : {winner}",True,(0, 150, 0))
        screen.blit(winner_text,(DEBUG_X, 850))
            
            

    pygame.display.flip()

pygame.quit()