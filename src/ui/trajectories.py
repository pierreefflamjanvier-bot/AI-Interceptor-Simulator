import pygame


def draw_trajectories(
    screen,
    target,
    interceptor_red,
    interceptor_blue,
    interceptor_green
):

    # ==========================================
    # TARGET
    # ==========================================

    if len(target.history) > 1:
        pygame.draw.lines(screen,(180, 180, 180),False,target.history,2)

    # ==========================================
    # PURE PURSUIT
    # ==========================================

    if len(interceptor_red.history) > 1:
        pygame.draw.lines(screen,(255, 50, 50),False,interceptor_red.history,2)

    # ==========================================
    # LEAD PURSUIT
    # ==========================================

    if len(interceptor_blue.history) > 1:
        pygame.draw.lines(screen,(0, 0, 255),False,interceptor_blue.history,2)

    # ==========================================
    # PROPORTIONAL NAVIGATION
    # ==========================================

    if len(interceptor_green.history) > 1:
        pygame.draw.lines(screen,(0, 180, 0),False,interceptor_green.history,2)
