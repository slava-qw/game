import pygame
import numpy as np
from balls import Ball, Balls
from config_of_grid import *


class Line:
    def __init__(self, x1, y1, x2, y2, color, width=4):
        self.x1 = x1
        self.y1 = y1
        self.line_start = (x1, y1)

        self.x2 = x2
        self.y2 = y2
        self.line_end = (x2, y2)

        self.width = width
        self.color = color

    def check_collision(self, circ, check_mode, eps=1e-3):
        """Check collision between one line and given ball"""

        (x1, y1), (x2, y2) = self.line_start, self.line_end
        x3, y3 = circ.x, circ.y
        a = np.array([x1 - x3, y1 - y3])
        b = np.array([x2 - x3, y2 - y3])

        x = (a.T @ a - a.T @ b) / (b.T @ b - a.T @ b)
        vec_h = 1 / (1 + x) * a + x / (1 + x) * b

        d1, d2 = np.linalg.norm(a - vec_h), np.linalg.norm(b - vec_h)
        ll = np.linalg.norm(a - b)
        if np.allclose(d1 + d2, ll, atol=1):
            coll_type = 1
        elif np.linalg.norm(a) < np.linalg.norm(b):
            coll_type = 2
            vec_h = a
        else:
            coll_type = 3
            vec_h = b

        d2 = vec_h.T @ vec_h

        # to draw all directions of the ball and all lines
        if check_mode:
            pygame.draw.line(circ.screen, (0, 122, 234), [circ.x, circ.y], np.array([circ.x, circ.y]) + vec_h, 2)
            pygame.draw.line(circ.screen, (2, 67, 34), [circ.x, circ.y], np.array([circ.x, circ.y]) + a, 2)
            pygame.draw.line(circ.screen, (2, 39, 41), [circ.x, circ.y], np.array([circ.x, circ.y]) + b, 2)

        coll = d2 + eps < circ.r ** 2

        if coll:
            # change ball's position
            if coll_type == 1:
                dh = circ.r - np.sqrt(d2)
                n = - vec_h / np.linalg.norm(vec_h)
                circ.x += ((dh + 2) * n)[0]
                circ.y += ((dh + 2) * n)[1]
            else:
                circ.x -= circ.velocity[0]
                circ.y -= circ.velocity[1]

            # change ball's velocity
            if coll_type == 1:
                vnx = (circ.velocity @ n) * n
                circ.velocity = -vnx + (circ.velocity - vnx)
            else:
                circ.velocity *= (-1)

                # cause some problems
                # use the formula of two-dimensional elastic collision with two moving objects
                # by substitute m2 = \inf, v2 = 0,
                # a1 = np.array(circ.xy)
                # a2 = a if coll_type == 2 else b
                # circ.velocity = v1 - 2 * (v1.T @ (a1 - a2)) / ((a1 - a2).T @ (a1 - a2)) * (a1 - a2)


class Lines(Line):
    def __init__(self, lines: list[Line], screen, check_mode: bool):
        self.lines = lines
        self.screen = screen
        self.check_mode = check_mode

    @staticmethod
    def draw_lines(screen, lines_n_flags):
        """Draw all lines that were placed on the screen"""

        list_of_lines, line_start, drawing = lines_n_flags

        if list_of_lines.lines:
            for fl in list_of_lines.lines:
                pygame.draw.line(screen, fl.color, fl.line_start, fl.line_end, fl.width)

        # Draw the current line if drawing (during mouse motions)
        if drawing and line_start:
            current_mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, white, line_start, current_mouse_pos, 2)

    def check_collisions(self, circ: Ball, lines: list[Line]=None):
        """Check collisions between the ball and all lines"""

        if lines is None:
            lines = self.lines

        for line in lines.lines:
            line.check_collision(circ, self.check_mode)

    def __len__(self):
        return len(self.lines)

    @classmethod
    def make_nozzle(cls, center=None):
        """Draw the nozzle boundaries"""

        if center is None:
            center = [WIDTH // 2 - 200, HEIGHT // 2]

        a = 50
        lines_left = [
            Line(
                center[0] - length / 2, center[1] - length / 2,
                center[0] - length / 2, center[1] + length / 2,
                red, 8
                 ),
            Line(
                center[0] - length / 2, center[1] - length / 2,
                center[0] + length / 2, center[1] - length / 2,
                red, 8
                 ),

            Line(
                center[0] + length / 2, center[1] - length / 2,
                center[0] + length / 2, center[1] - a,
                red, 8
                 ),
            Line(
                center[0] + length / 2, center[1] + a,
                center[0] + length / 2, center[1] + length / 2,
                red, 8
                ),
            Line(
                center[0] + length / 2, center[1] + length / 2,
                center[0] - length / 2, center[1] + length / 2,
                red, 8
                 ),
        ]

        lines_right = [
            Line(
                center[0] + 3 * length / 2, center[1] - length / 2,
                center[0] + 3 * length / 2, center[1] + length / 2,
                red, 8
                ),
            Line(
                center[0] + length / 2, center[1] - length / 2,
                center[0] + 3 * length / 2, center[1] - length / 2,
                red, 8
                ),
            Line(
                center[0] + 3 * length / 2, center[1] + length / 2,
                [center[0] + length / 2, center[1] + length / 2],
                red, 8
                ),
        ]

        return lines_left
