import pygame


def draw_debug_panel(screen,font,DEBUG_X,sensor,track,interceptor_red,interceptor_blue,interceptor_green,target_visible):

    # ==================================================
    # TITRE
    # ==================================================

    debug_title = font.render("DEBUG PANEL",True,(0, 0, 0))

    screen.blit(debug_title,(DEBUG_X, 20))
        
        

    # ==================================================
    # LEGENDE
    # ==================================================

    screen.blit(font.render("Noir : Cible",True,(0, 0, 0)),(DEBUG_X, 60))
    screen.blit(font.render("Rouge : Pure Pursuit",True,(255, 0, 0)),(DEBUG_X, 100))

    screen.blit(font.render("Bleu : Lead Pursuit",True,(0, 0, 255)),(DEBUG_X, 140))

    screen.blit(font.render("Vert : Proportional Navigation",True,(0, 180, 0)),(DEBUG_X, 180))

    # ==================================================
    # SENSOR
    # ==================================================

    sensor_title = font.render("-----SENSOR-----",True,(0, 0, 0))

    screen.blit(sensor_title,(DEBUG_X, 250))

    if target_visible:
        visibility_text = font.render("VISIBLE",True,(0, 180, 0))
        if sensor.visual_lock:
            lock_text = font.render("VISUALLOCKED",True,(0, 180, 255))
        else:
            lock_text = font.render("TRACK MODE",True,(255, 0, 0))
    else:
        visibility_text = font.render("LOST",True,(255, 0, 0))

    screen.blit(visibility_text,(DEBUG_X, 290))
    screen.blit(lock_text,(DEBUG_X, 310))

    angle_text = font.render(f"Angle Error:{sensor.last_angle_error:.1f}°",True,(255, 255, 0))

    screen.blit(angle_text,(DEBUG_X, 330))

    # ==================================================
    # TRACK
    # ==================================================

    track_title = font.render("-----TRACK-----",True,(0, 0, 0))

    screen.blit(track_title,(DEBUG_X, 410))

    if not track.valid:
        track_status_text = "TRACK LOST"
        track_color = (255, 0, 0)
    elif track.predicted:
        track_status_text = "TRACK PREDICTED"
        track_color = (255, 165, 0)
    else:
        track_status_text = "TRACK VALID"
        track_color = (0, 255, 0)

    track_status_surface = font.render(track_status_text,True,track_color)
    screen.blit(track_status_surface,(DEBUG_X, 450))

    track_position = font.render(f"Track : ({track.x:.1f},{track.y:.1f})",True,(255, 0, 255))
    screen.blit(track_position,(DEBUG_X, 490))

    confidence_text = font.render(f"Confidence:{track.confidence:.0f}%",True,(255, 0, 0))
    screen.blit(confidence_text,(DEBUG_X, 530))

    prediction_age_text = font.render(f"Prediction Age:{track.time_since_measurement:.1f}s",True,(255, 255, 0))
    screen.blit(prediction_age_text,(DEBUG_X, 570))

    # ==================================================
    # INTERCEPTORS
    # ==================================================

    interceptor_title = font.render("-----INTERCEPTORS-----",True,(0, 0, 0))
    screen.blit(interceptor_title,(DEBUG_X, 650))

    heading_red = font.render(f"Cap Rouge:{interceptor_red.heading:.1f}",True,(255, 0, 0))
    screen.blit(heading_red,(DEBUG_X, 700))

    heading_blue = font.render(f"Cap Bleu:{interceptor_blue.heading:.1f}",True,(0, 0, 255))
    screen.blit(heading_blue,(DEBUG_X, 740))

    heading_green = font.render(f"Cap Vert:{interceptor_green.heading:.1f}",True,(0, 180, 0))

    screen.blit(heading_green,(DEBUG_X, 780))