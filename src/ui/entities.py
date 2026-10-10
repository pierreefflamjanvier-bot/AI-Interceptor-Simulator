import pygame
import math


def draw_entities(
    screen,
    target,
    interceptor_red,
    interceptor_blue,
    interceptor_green,
    measurement,
    track,
    target_visible
):

    # ==========================================
    # TARGET
    # ==========================================

    pygame.draw.circle(screen,(0, 0, 0),(int(target.x), int(target.y)),8)

    # ==========================================
    # PURE PURSUIT
    # ==========================================

    pygame.draw.circle(screen,(255, 0, 0),(int(interceptor_red.x), int(interceptor_red.y)),8)
    line_length = 30
    end_x = (interceptor_red.x+line_length*math.cos(math.radians(interceptor_red.heading)))
    end_y = (interceptor_red.y+line_length*math.sin(math.radians(interceptor_red.heading)))

    pygame.draw.line(screen,(255, 0, 0),(int(interceptor_red.x), int(interceptor_red.y)),(int(end_x), int(end_y)),2)

    # ==========================================
    # LEAD PURSUIT
    # ==========================================

    pygame.draw.circle(screen,(0, 0, 255),(int(interceptor_blue.x), int(interceptor_blue.y)),8)

    # ==========================================
    # PROPORTIONAL NAVIGATION
    # ==========================================

    pygame.draw.circle(screen,(0, 180, 0),(int(interceptor_green.x), int(interceptor_green.y)),8)

    # ==========================================
    # SENSOR MEASUREMENT
    # ==========================================

    if measurement is not None:

        pygame.draw.circle(screen,(255, 165, 0),(int(measurement[0]), int(measurement[1])),4)

    # ==========================================
    # TRACK
    # ==========================================

    if target_visible:
        track_color = ((255, 165, 0) if track.predicted else (255, 0, 255))
        pygame.draw.circle(screen,track_color,(int(track.x),int(track.y)),4)