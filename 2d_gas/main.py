import sys
import pygame
import numpy as np

from config_of_grid import *
from lines import Line, Lines
from balls import Balls
from real_time_graphs import RealTimeGraph


def check_collisions(*args, mode='b2b'):
    """
    Check collisions depending on the mode and fix them
    :param args: which objects we want to check
    :param mode: define the type of collisions:
        b2b - ball to ball,
        b2w - ball to wall,
        b2f - ball to frame boundaries
    :param eps: precision of collision
    :return: bool or None
    """

    if mode == 'b2b':
        circ1, circ2 = args
        return Balls.check_collisions(circ1, circ2)

    elif mode == 'b2w':
        circ, lines = args
        lines.check_collisions(circ, lines)

    elif mode == 'b2f':
        circ = args[0]
        if (st11 := circ.x - circ.r < 0) or (st12 := circ.x + circ.r > WIDTH):
            circ.velocity[0] *= -1
            circ.x = circ.r if st11 else (WIDTH - circ.r if st12 else circ.x)

        if (st21 := circ.y - circ.r < 0) or (st22 := circ.y + circ.r > HEIGHT):
            circ.velocity[1] *= -1
            circ.y = circ.r if st21 else (HEIGHT - circ.r if st22 else circ.y)


def update(circs, lines: Lines, graphs):
    """
    Update the position of the balls as well as velocities, check collisions and fix them.
    Also, calculate some statistics for graphs.
    """

    vel_line_graph, abs_v_graph = graphs

    for circ in circs.balls:
        circs.change_velocity(circ, circs)  # for collisions of balls

        # make a 'step' for each ball
        circ.x += circ.velocity[0]
        circ.y += circ.velocity[1]

        if check_mode:
            # FIXME
            screen.fill((0, 0, 0))  # for drawing vectors of direction

        if len(lines):
            check_collisions(circ, lines, mode='b2w')  # for walls and balls

        check_collisions(circ, mode='b2f')  # for boundaries and balls

        circ.check_isin(lines)
        abs_v_graph.add_data_point(np.linalg.norm(circ.velocity))

    in_balls = circs.q_isin()
    v_out = circs.v_out()
    mean_out_v = np.mean(v_out, axis=0)[0] if len(v_out) else 0

    vel_line_graph.add_data_point(mean_out_v)


def render(screen, fps, circs, lines_n_flags, graphs):
    vel_line_graph, abs_v_graph = graphs

    if not check_mode:
        screen.fill((0, 0, 0))

    lines_n_flags[0].draw_lines(screen, lines_n_flags)

    for circ in circs.balls:
        pygame.draw.circle(screen, circ.color, list(map(int, [circ.x, circ.y])), circ.r, 0)

        # for velocity vectors
        # pygame.draw.line(screen, (255, 255, 255), [circ.x, circ.y], 15 * np.array(circ.velocity) + np.array([circ.x, circ.y]), 3)

    vel_line_graph.draw(screen)  # Draw the graph on the smaller surface
    abs_v_graph.draw(screen)

    pygame.display.update()
    fps.tick(60)  # Do not update the screen more than 60 times per second


def init():
    pygame.init()
    pygame.display.set_caption("2D Gas Simulation")
    screen = pygame.display.set_mode(SCREEN_SIZE)

    vel_line_graph = RealTimeGraph(270 / 40 * 50, 200 / 50 * 50 * 1.05, [20, 20], 'line')
    abs_v_graph = RealTimeGraph(270 / 40 * 50, 200 / 50 * 50 * 1.05, [20, 250], 'hist')

    N = 100
    circs = Balls(N, screen, mode='1bb')
    circs.sort(key=lambda circ: -circ.r)  # We sort so that the big ones do not obscure the small ones

    drawing = False
    line_start = None
    final_lines = Lines([], screen, check_mode)

    nozzle_bnds = final_lines.make_nozzle(center=center)
    final_lines.lines.extend(nozzle_bnds)

    return screen, circs, drawing, final_lines, line_start, [vel_line_graph, abs_v_graph]


if __name__ == '__main__':
    screen, circs, drawing, final_lines, line_start, graphs = init()

    fps = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_r:  # for restart
                    screen, circs, drawing, final_lines, line_start, graphs = init()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    drawing = True
                    line_start = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                line_end = pygame.mouse.get_pos()

                if line_start and line_end:
                    final_lines.lines.append(Line(*line_start, *line_end, green, 4))

        update(circs, final_lines, graphs)  # change all coordinates and calc other things
        render(screen, fps, circs, [final_lines, line_start, drawing], graphs)  # draw everything
