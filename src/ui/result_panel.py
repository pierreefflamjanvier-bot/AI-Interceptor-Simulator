import pygame


def draw_results_panel(
    screen,
    font,
    DEBUG_X,
    interceptor_red,
    interceptor_blue,
    interceptor_green,
    simulation_finished
):

    results_title = font.render("-----RESULTS-----",True,(0, 0, 0))
    screen.blit(results_title,(DEBUG_X, 820))

    if interceptor_red.interception_time is not None:
        pure_text = font.render(f"Pure : {interceptor_red.interception_time:.2f} s",True,(255, 0, 0))
        screen.blit(pure_text,(DEBUG_X, 860))

    if interceptor_blue.interception_time is not None:
        lead_text = font.render(f"Lead : {interceptor_blue.interception_time:.2f} s",True,(0, 0, 255))
        screen.blit(lead_text,(DEBUG_X, 900))

    if interceptor_green.interception_time is not None:
        pn_text = font.render(f"Proportional : {interceptor_green.interception_time:.2f} s",True,(0, 180, 0))
        screen.blit(pn_text,(DEBUG_X, 940))

    if not simulation_finished:
        return

    winner = "EGALITE"

    if (
        interceptor_red.interception_time is not None
        and interceptor_blue.interception_time is not None
        and interceptor_green.interception_time is not None
    ):

        if (
            interceptor_red.interception_time
            < interceptor_blue.interception_time
            and interceptor_red.interception_time
            < interceptor_green.interception_time
        ):

            winner = "PURE PURSUIT"

        elif (
            interceptor_blue.interception_time
            < interceptor_red.interception_time
            and interceptor_blue.interception_time
            < interceptor_green.interception_time
        ):

            winner = "LEAD PURSUIT"

        elif (
            interceptor_green.interception_time
            < interceptor_red.interception_time
            and interceptor_green.interception_time
            < interceptor_blue.interception_time
        ):

            winner = "PROPORTIONAL NAVIGATION"

    winner_text = font.render(f"Gagnant : {winner}",True,(0, 150, 0))
    screen.blit(winner_text,(DEBUG_X-500,900 ))