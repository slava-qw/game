from config_of_grid import *
from random import randint, uniform
import numpy as np
import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self,
                 id: int, x: int, y: int, r: int,
                 color: np.array,
                 velocity: np.array,
                 mass: [float | int],
                 screen
                 ):


        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.velocity = velocity
        self.mass = mass
        self.screen = screen

        self.image = pygame.Surface((2 * self.r, 2 * self.r), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def check_isin(self, lines) -> bool:
        """
        For a given set of lines that made up a convex polygon
        check if the ball is in that polygon

        from here: https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not
        """

        # for a box shape polygon (with one hole) just simplify it
        c = 0
        for line in lines.lines:
            c = max(c, line.x1, line.x2)

        self.isin = self.x <= c


class Balls(Ball):
    def __init__(self, N, screen, mode):
        self.N = N
        self.screen = screen
        self.mode = mode

        self.balls: list[Ball] = self.make_balls(self.N)  # change the type of view of this func
        self.id2balls = {id: ball for id, ball in enumerate(sorted(self.balls, key=lambda ball: ball.id))}

    def make_balls(self, N: int) -> list[Ball]:
        # FIXME: change coordinates of the balls

        if self.mode == '2b':

            self.circs_1 = [Ball(id,
                                 center[0] + randint(-50 // 2, 50 // 2),
                                 center[1] + randint(-50 // 2, 50 // 2),
                                 10, red, np.array([uniform(-10, 10), uniform(-10, 10)]),
                                 1, self.screen)
                            for id in range(N)]

            self.circs_2 = [Ball(id,
                                 WIDTH // 2 + 250 + randint(-50 // 2, 50 // 2),
                                 HEIGHT // 2 + randint(-50 // 2, 50 // 2),
                                 10, red, np.array([uniform(-3, 3), uniform(-3, 3)]),
                                 1, self.screen)
                            for id in range(N)]

            self.balls = self.circs_1 + self.circs_2

        elif self.mode == '1bb':
            self.circs = [Ball(id,
                               center[0] + randint(-50 // 2, 50 // 2),
                               center[1] + randint(-50 // 2, 50 // 2),
                               10, red, np.array([uniform(-10, 10), uniform(-10, 10)]),
                               1, self.screen)
                          for id in range(N)]

            # big_circ = Ball(N + 1,
            #                 100, 400,  # [uniform(300, 321), uniform(200, 230)],
            #                 100, [randint(0, 255), randint(0, 255), randint(0, 255)],
            #                 [uniform(-5, 5), uniform(-5, 5)],
            #                 100, self.screen)
            # self.circs.append(big_circ)

            self.balls = self.circs

        return self.balls

    def sort(self, key):
        self.balls.sort(key=key)

    @classmethod
    def change_pos(cls, circ1: Ball, circ2: Ball) -> tuple[np.array, np.array, np.array]:
        """
        change position of circ1 and circ2 that they both touch only each other and not overlap
        """
        a1, a2 = np.array([circ1.x, circ1.y]), np.array([circ2.x, circ2.y])
        d = np.sqrt((circ1.x - circ2.x) ** 2 + (circ1.y - circ2.y) ** 2)
        r1, r2 = circ1.r, circ2.r
        cosa = (r1 ** 2 + d ** 2 - r2 ** 2) / (2 * r1 * d)
        cosb = (r2 ** 2 + d ** 2 - r1 ** 2) / (2 * r2 * d)
        dc1 = r1 * (1 - cosa)
        dc2 = r2 * (1 - cosb)
        c = a2 - a1
        nc = c / np.linalg.norm(c)

        return nc, dc1, dc2

    @classmethod
    def check_collisions(cls, circ1, circ2) -> bool:
        if (circ1.x - circ2.x) ** 2 + \
                (circ1.y - circ2.y) ** 2 < (circ1.r + circ2.r) ** 2:
            return True

    @classmethod
    def change_velocity(cls, circ, circs):
        """
        Change both the position of the collision balls and their velocities
        """
        for other_circ in circs.balls:
            if circ.id != other_circ.id and cls.check_collisions(circ, other_circ):
                nc, dc1, dc2 = cls.change_pos(circ, other_circ)

                m1, m2 = circ.mass, other_circ.mass
                v1, v2 = np.array(circ.velocity), np.array(other_circ.velocity)

                a1, a2 = np.array([circ.x, circ.y]) - nc * dc1, np.array([other_circ.x, other_circ.y]) + nc * dc2

                # from here: https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects
                # and here: https://new.math.uiuc.edu/math198/MA198-2013/dprorok2/documentation.pdf
                w1 = v1 - 2 * m2 / (m1 + m2) * ((v1 - v2).T @ (a1 - a2)) / ((a1 - a2).T @ (a1 - a2)) * (a1 - a2)
                w2 = v2 - 2 * m1 / (m1 + m2) * ((v2 - v1).T @ (a2 - a1)) / ((a2 - a1).T @ (a2 - a1)) * (a2 - a1)

                circ.velocity = w1
                other_circ.velocity = w2

                circ.x -= (nc * (dc1 + 1))[0]
                circ.y -= (nc * (dc1 + 1))[1]
                other_circ.x += (nc * (dc2 + 1))[0]
                other_circ.y += (nc * (dc2 + 1))[1]

    def q_isin(self) -> list:
        """Return the number of balls that are located inside the nozzle"""

        self.in_balls = []
        for circ in self.balls:
            if circ.isin:
                self.in_balls.append(circ.id)

        return self.in_balls

    def v_out(self) -> np.array:
        """Calculate some statistics (here velocities) for balls that are located outside the nozzle"""

        out_velocities = []
        for id in ({i for i in range(self.N)} - set(self.in_balls)):
            out_velocities.append(self.id2balls[id].velocity.tolist())

        out_velocities = np.array(out_velocities)
        return out_velocities
