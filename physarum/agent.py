from copy import deepcopy
import numpy as np
from scipy.spatial import distance
import config as cfg

import pygame as pg


class Plane:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.m = np.zeros((self.h, self.w))

    @staticmethod
    def circular_mask_func(array: np.array, center: np.array, radius: int or list, mask_type: int = 1) -> np.array:
        # Get the indices of all elements in the array
        # array = array.copy()
        indices = np.indices(array.shape)
        # Calculate the Euclidean distance from each element to the center of the circle
        distances = np.linalg.norm(indices - center[:, np.newaxis, np.newaxis], axis=0)
        # Mask elements outside the specified radius
        if mask_type == 2:
            r1, r2 = radius
            mask = r1 <= distances <= r2
            return mask

        mask = distances <= radius
        return mask

    def increase_score(self, rect, score):
        """Increase the score in the circle only for head"""
        # make the circle instead of rectangle
        r = rect.centerx - rect.x
        c = self.m[rect.y:rect.y + 2 * r, rect.x:rect.x + 2 * r]
        # Apply the circular mask function
        rel_center = np.array(rect.center) - np.array([rect.x, rect.y])
        mask = self.circular_mask_func(c, rel_center, r)  # mask has the same shape as c
        self.m[rect.y:rect.y + 2 * r, rect.x:rect.x + 2 * r][mask] += score

    def decrease_score(self, rect, score, i):
        # TODO: make the diffusion of the score circle

        r = rect.centerx - rect.x  # + min(i, 5)
        c = self.m[rect.y:rect.y + 2 * r, rect.x:rect.x + 2 * r]
        # Apply the circular mask function
        rel_center = np.array(rect.center) - np.array([rect.x, rect.y])
        mask = self.circular_mask_func(c, rel_center, r)  # mask has the same shape as c

        f = np.vectorize(lambda x, s: max(0, x - s))
        self.m[rect.y:rect.y + 2 * r, rect.x:rect.x + 2 * r][mask] = f(c, score)[mask]

    def set_score(self, rect, score):
        raise NotImplemented('Change to circular_mask_func')

        # make the circle instead of rectangle
        r = rect.centerx - rect.x
        self.m[rect.y:rect.y + 2 * r, rect.x:rect.x + 2 * r] = score

    def calculate_score(self, sensors: list[tuple[int]]) -> list[int]:
        """
        :param sensors: contain pairs of (x, y) coordinates of each sensor
        :return: score for each sensor
        """
        d = []
        # make parallel
        for i, sensor in enumerate(sensors):
            d.append(self.m[int(sensor[1]) % self.h, int(sensor[0]) % self.w])
        return d

    def draw(self, sc):
        pass


class Agent:
    def __init__(self, x, y, v, alpha, r, g, surface, plane):
        self.plane = plane
        self.display_surface = surface
        # it needs for a real-time display, but after some time it raises some OOM error, idk why...
        # self.w2 = self.display_surface.convert_alpha()
        # self.w2.fill([0, 0, 0, 0])

        self.h = cfg.h
        self.w = cfg.w
        self.x = x
        self.y = y
        self.v = v
        self.alpha = alpha
        self.d_alpha = np.pi / 24
        self.r = r
        self.al = 250
        self.max_score = 500 * self.al
        self.dr = 1
        self.d_al = 1

        # for checker settings
        self.l = 5.5
        self.n = 3  # should be odd
        self.g = g

    def copy(self):
        return Agent(self.x, self.y, self.v, self.alpha, self.r, self.g, self.display_surface, self.plane)

    def get_rect(self):
        return pg.Rect(self.x, self.y, 2 * self.r, 2 * self.r)

    def draw(self):
        # raise Exception('Can cause some problems with OOM errors, uncomment self.w2 and self.w2.fill([0, 0, 0, 0])')
        # we here, only if self.al >= 0
        pg.draw.circle(self.w2, (255, 127, 80, self.al), (self.r, self.r), radius=self.r)
        # pg.draw.rect(self.w2, (0, 0, 0, 200), (0, 0, self.r, self.r))
        self.display_surface.blit(self.w2, (self.x, self.y))

    @staticmethod
    def calculate_angle(vector1, vector2=np.array([1, 0])):
        dot_product = np.dot(vector1, vector2)
        norm_vector1 = np.linalg.norm(vector1)
        norm_vector2 = np.linalg.norm(vector2)
        cosine_angle = dot_product / (norm_vector1 * norm_vector2)
        angle = np.arccos(cosine_angle)  # in radians
        return angle

    def move_head(self):
        # we can be here only if it's the head of our tail
        self.make_checker()
        # to draw the sensors
        # self.draw_sensors()

        d = self.plane.calculate_score(self.sensor_coordinates)
        if sum(d) == 0:
            # random moving without sensors
            z = np.random.normal(0, 1, 1)
            if z < -1.5:
                self.alpha -= np.pi / 3
            elif z > 1.5:
                self.alpha += np.pi / 3
        else:
            # choose the direction
            max_d = max(d)
            if max_d <= self.max_score:  # if there are so many score agent chooses the min score-direction
                dir = self.sensor_coordinates[d.index(max_d)]
            else:
                dir = self.sensor_coordinates[d.index(min(d))]

            dir_as_v = np.array([dir[0], dir[1]])
            dir_to_move = dir_as_v - np.array([self.x + self.r, self.y + self.r])

            zz = np.random.rand()
            if zz > 0.25:
                # with 75% prob it goes towards the sensor direction
                self.alpha = self.calculate_angle(dir_to_move)
            else:
                # random moving without sensors
                z = np.random.normal(0, 1, 1)
                if z < -1.5:
                    self.alpha -= np.pi / 3
                elif z > 1.5:
                    self.alpha += np.pi / 3

        self.alpha += np.random.uniform(-self.d_alpha, self.d_alpha)  # to add some randomness
        self.x = (self.x + self.v * np.cos(self.alpha)) % self.w
        self.y = (self.y + self.v * np.sin(self.alpha)) % self.h

        # for another type of bounds
        # if self.y - self.r < 7:
        #     self.alpha *= -1
        # if self.y + self.r > self.h - 7:
        #     self.alpha *= -1
        # if self.x - self.r < 7:
        #     self.alpha = PI - self.alpha
        # if self.x + self.r > self.w - 7:
        #     self.alpha = PI - self.alpha

        # self.x += self.v * cos(self.alpha)
        # self.y += self.v * sin(self.alpha)

    def decrease_al(self):
        # self.r -= self.dr
        self.al -= self.d_al

    def make_checker(self):
        r = self.l + self.r
        # absolute coordinate in xy plane (in self.display_surface)
        self.sensor_coordinates = [
            (self.r + self.x + r * np.cos(self.alpha + self.g), self.r + self.y + r * np.sin(self.alpha + self.g)),
            (self.r + self.x + r * np.cos(self.alpha), self.r + self.y + r * np.sin(self.alpha)),
            (self.r + self.x + r * np.cos(self.alpha - self.g), self.r + self.y + r * np.sin(self.alpha - self.g))
        ]

    def draw_sensors(self):
        r = 3
        for x, y in self.sensor_coordinates:
            pg.draw.circle(self.display_surface, 'red', (x, y), radius=r)


class Trail:
    def __init__(self):
        self.trail = []

    def add_to_trail(self, circ):
        self.trail.append(circ)

    def draw(self):
        # execution of this function happens each frame
        s = list(self.trail)

        # make parallel
        for i, circ in enumerate(s[::-1]):
            if circ.al >= 0:
                circ.plane.decrease_score(circ.get_rect(), circ.d_al, i)
                if i == 0:
                    # here i == 0
                    circ.plane.increase_score(circ.get_rect(), circ.al)
                    # make condition for the stroke of the trail's head
                    # circ.draw()  # to draw only the head

                    circ.move_head()
                    self.add_to_trail(circ.copy())
                # else:
                    # circ.draw()
            else:
                # circ.plane.set_score(circ.get_rect(), 0)
                c = self.trail.pop(0)
            circ.decrease_al()

    def get_trail(self):
        return self.trail


def draw_all(T):
    T.draw()
