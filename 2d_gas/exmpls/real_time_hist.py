import pygame
import sys
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
from scipy.stats import norm

pygame.init()

# Create a larger window
main_width, main_height = 1200, 800
main_window = pygame.display.set_mode((main_width, main_height))
pygame.display.set_caption('Main Window')

# Create a smaller surface for the real-time graph
graph_width, graph_height = 800, 600
graph_surface = pygame.Surface((graph_width, graph_height))
graph_surface_rect = graph_surface.get_rect()
graph_surface_rect.topleft = (20, 20)  # Adjust the position as needed

class RealTimeGraph:
    def __init__(self, max_data_points=100):
        self.data = []
        self.max_data_points = max_data_points
        self.fig, self.ax = plt.subplots(figsize=(graph_width / 100, graph_height / 100), dpi=100)

    def add_data_point(self, value):
        self.data.append(value)
        if len(self.data) > self.max_data_points:
            self.data.pop(0)

    def draw(self, surface):
        # Draw the histogram and approximation line on the given surface using Matplotlib
        self.ax.clear()
        self.ax.hist(self.data, bins=np.linspace(0, 100, 20), color='black', edgecolor='white', density=True)

        # Fit a normal distribution to the data
        mu, std = norm.fit(self.data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        self.ax.plot(x, p, 'r', linewidth=2)

        self.ax.set_xlabel('Mean X Velocity', fontsize=14)
        self.ax.set_ylabel('Density', fontsize=14)
        self.ax.set_title('Real-Time Histogram with Approximation', fontsize=16)

        # Customize the appearance further if needed

        canvas = FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        # Convert Matplotlib surface to Pygame surface
        graph_surface = pygame.image.fromstring(raw_data, size, "RGB")

        # Blit the Matplotlib surface onto the Pygame surface
        surface.blit(graph_surface, (0, 0))

    def get_points(self):
        # Calculate the screen coordinates for each data point
        x_step = graph_width / max(len(self.data) - 1, 1)
        return [(int(i * x_step), int(graph_height - (value / 100.0 * graph_height))) for i, value in enumerate(self.data)]

graph = RealTimeGraph()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    new_data_point = random.randint(0, 100)  # Replace this with your real-time data
    graph.add_data_point(new_data_point)

    graph_surface.fill((255, 255, 255))  # Set background color to white
    graph.draw(graph_surface)  # Draw the histogram and approximation line on the smaller surface
    main_window.fill((255, 255, 255))  # Set background color to white
    main_window.blit(graph_surface, graph_surface_rect.topleft)  # Blit the smaller surface onto the main window
    pygame.display.flip()

    clock.tick(30)
