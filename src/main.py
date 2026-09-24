import pygame
import math

from entities.target import Target
from entities.interceptor import Interceptor

from guidance.pure_pursuit import PurePursuit
from guidance.lead_pursuit import LeadPursuit
from guidance.proportional_navigation import ProportionalNavigation


# ==================================================
# INITIALISATION
# ==================================================

pygame.init()

WIDTH, HEIGHT = 1200, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Interceptor Simulator")

font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()


# ==================================================
# ENTITES
# ==================================================

target = Target(x=900,y=400,vx=-160,vy=60)
interceptor_red = Interceptor(x=200,y=200,speed=150,strategy=PurePursuit())
interceptor_blue = Interceptor(x=200,y=200,speed=150,strategy=LeadPursuit())
interceptor_green = Interceptor(x=200,y=200,speed=150,strategy=ProportionalNavigation())    

# ==================================================
# VARIABLES
# ==================================================

running = True
elapsed_time = 0
simulation_finished = False

distance_red = 0
distance_blue = 0
distance_green = 0


# ==================================================
# BOUCLE PRINCIPALE
# ==================================================

while running:

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

    if not simulation_finished:

        elapsed_time += dt

        target.update(dt)

        if not interceptor_red.finished:
            interceptor_red.update(dt, target)

        if not interceptor_blue.finished:
            interceptor_blue.update(dt, target)

        if not interceptor_green.finished:
            interceptor_green.update(dt, target)

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
        
    pygame.draw.circle(screen,(0, 0, 255),(int(interceptor_blue.x), int(interceptor_blue.y)),8)

    pygame.draw.circle(screen,(0, 180, 0),(int(interceptor_green.x), int(interceptor_green.y)),8)   
        
    # ----------------------------------------------
    # CHRONO
    # ----------------------------------------------

    timer_text = font.render(f"Temps : {elapsed_time:.2f} s",True,(0, 0, 0))
    screen.blit(timer_text,(20, 20))


    # ----------------------------------------------
    # LEGENDE
    # ----------------------------------------------

    screen.blit(font.render("Noir : Cible",True,(0, 0, 0)),(20, 60))
    screen.blit(font.render("Rouge : Pure Pursuit",True,(255, 0, 0)),(20, 100))
    screen.blit(font.render("Bleu : Lead Pursuit",True,(0, 0, 255)),(20, 140))
    screen.blit(font.render("Vert : Proportional Navigation",True,(0, 180, 0)),(20, 180)) 

    # ----------------------------------------------
    # RESULTATS
    # ----------------------------------------------

    if interceptor_red.interception_time is not None:
        screen.blit(font.render(f"Pure : "f"{interceptor_red.interception_time:.2f} s",True,(255, 0, 0)),(900, 60))

    if interceptor_blue.interception_time is not None:
        screen.blit(font.render(f"Lead : "f"{interceptor_blue.interception_time:.2f} s",True,(0, 0, 255)),(900, 100))

    if interceptor_green.interception_time is not None:
        screen.blit(font.render(f"Proportional : "f"{interceptor_green.interception_time:.2f} s",True,(0, 180, 0)),(900, 140))  

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
        screen.blit(winner_text,(600, 750))
            
            

    pygame.display.flip()

pygame.quit()