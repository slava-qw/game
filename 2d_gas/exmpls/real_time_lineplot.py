import pygame
import sys
import random
from config_of_grid import *

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Real-Time Graph')


class RealTimeGraph:
    def __init__(self, max_data_points=100):
        self.data = []
        self.max_data_points = max_data_points

    def add_data_point(self, value):
        self.data.append(value)
        if len(self.data) > self.max_data_points:
            self.data.pop(0)

    def draw(self, surface, color=(255, 255, 255)):
        # Draw the graph on the given surface
        points = self.get_points()
        if len(points) > 1:
            pygame.draw.lines(surface, color, False, points, 2)

    def get_points(self):
        # Calculate the screen coordinates for each data point
        x_step = WIDTH / max(len(self.data) - 1, 1)
        return [(int(i * x_step), int(height - (value / 100.0 * height))) for i, value in enumerate(self.data)]


graph = RealTimeGraph()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    new_data_point = random.randint(0, 100)  # Replace this with your real-time data
    graph.add_data_point(new_data_point)

    window.fill((0, 0, 0))
    graph.draw(window)
    pygame.display.flip()

    clock.tick(30)
