import pygame
import math

from entities.target import Target
from entities.interceptor import Interceptor
from guidance.pure_pursuit import PurePursuit

pygame.init()
WIDTH, HEIGHT = 1200, 800
font = pygame.font.SysFont(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Interceptor Simulator")

clock=pygame.time.Clock()
#Entities
target=Target(x=900, y=400, vx=-80, vy=30)
interceptor=Interceptor(x=200, y=200, speed=150, strategy=PurePursuit())

running = True
elapsed_time=0
simulation_finished= False
Interception_time=None

while running:
    dt = clock.tick(60) / 1000
    elapsed_time += dt
#Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#Update
    if not simulation_finished:
        elapsed_time+=dt
        target.update(dt)
        interceptor.update(dt, target)
    if not simulation_finished:
        distance= math.sqrt((target.x-interceptor.x)**2+(target.y-interceptor.y)**2)
        if distance<10:
            simulation_finished=True
            Interception_time=elapsed_time
            print(f"Interception réussie en {elapsed_time:.2f} secondes")
            
#affichage
    screen.fill((255,255,255))
#target trajectory
    if len(target.history)>1:
        pygame.draw.lines(screen, (180,180,180), False, target.history, 2)
#Interceptpr trajectory
    if len(interceptor.history)>1:
        pygame.draw.lines(screen, (255,50,50), False, interceptor.history, 2)

#Target
    pygame.draw.circle(screen, (0,0,0), (int(target.x), int(target.y)), 8)
#Interceptor
    pygame.draw.circle(screen, (255,0,0), (int(interceptor.x), int(interceptor.y)), 8)

    if simulation_finished:
        displayed_time=Interception_time
    else:
        displayed_time=elapsed_time

    timer_text = font.render(f"Temps : {displayed_time:.2f} s",True,(0, 0, 0))
    distance_text= font.render(f"Distance : {distance:.2f} px", True, (0, 0, 0)) 
    screen.blit(timer_text, (20, 140))
    screen.blit(distance_text, (20, 180))   

    status="EN COURS"
    if simulation_finished:
        status="INTERCEPTE"
    status_text=font.render(status,True,(0,150,0))
    screen.blit(status_text,(20,700))

    legend_target=font.render("Noir : Cible", True, (0, 0, 0))
    screen.blit(legend_target, (20, 60))

    legend_interceptor=font.render("Rouge : Intercepteur", True, (255, 0, 0))
    screen.blit(legend_interceptor, (20, 100))

    if simulation_finished:
        result_text=font.render(f"Interception réussie en {Interception_time:.2f} s", True, (0, 150, 0))
        screen.blit(result_text, (400,20))
    pygame.display.flip()
pygame.quit()