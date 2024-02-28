import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from sklearn.neighbors import KernelDensity

from config_of_grid import *


class RealTimeGraph:
    def __init__(self,
                 graph_width, graph_height,
                 coords: list[int, int],
                 type: str,
                 max_data_points=100):

        self.data = []
        self.max_data_points = max_data_points
        self.type = type

        self.coords = coords
        self.graph_width = graph_width
        self.graph_height = graph_height

        # Create a smaller surface for the real-time graph
        self.graph_surface = pygame.Surface((self.graph_width, self.graph_height))
        self.graph_surface_rect = self.graph_surface.get_rect()
        self.graph_surface_rect.topleft = self.coords  # Adjust the position as needed

        self.fig, self.ax = plt.subplots(figsize=(270 / 40, 200 / 50), dpi=50)  # some luck to choose the right sizes

    def add_data_point(self, value):
        self.data.append(value)
        if len(self.data) > self.max_data_points:
            self.data.pop(0)

    @staticmethod
    def kde_sklearn(x, x_grid, bandwidth=0.2, **kwargs):
        """Kernel Density Estimation with Scikit-learn"""

        kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
        kde_skl.fit(x[:, np.newaxis])

        # score_samples() returns the log-likelihood of the samples
        log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
        return np.exp(log_pdf)

    def draw(self, screen):
        self.graph_surface.fill(white)  # Set background color to white

        # Draw the graph on the given surface using Matplotlib
        self.ax.clear()

        if self.type == 'line':
            self.ax.plot(range(len(self.data)), self.data, color='black', linewidth=2)
            x_label = 'Time'
            y_label = 'Mean x-velocity'
            title = r'Outside x-mean velocity ($t$)'
        elif self.type == 'hist':
            # from here: https://stackoverflow.com/questions/66151692/pyplot-draw-a-smooth-curve-over-a-histogram,
            # https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/,
            # https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html

            self.ax.hist(self.data, bins=np.linspace(0, 20, 20), color='black', edgecolor='white', density=True)
            x_grid = np.linspace(-1, 20, 100)

            # Draw points from a bimodal distribution in 1D

            # use a rule-of-thumb from this:
            # https://en.wikipedia.org/wiki/Kernel_density_estimation#A_rule-of-thumb_bandwidth_estimator
            bandwidth = 1.06 * np.std(self.data) * len(self.data) ** (-1 / 5)
            pdf = self.kde_sklearn(np.array(self.data).T, x_grid, bandwidth=bandwidth)
            self.ax.plot(x_grid, pdf, color='red', alpha=0.5, lw=3)

            x_label = 'Abs velocity'
            y_label = 'Density'
            title = r'hist of v-abs'

        self.ax.set_xlabel(x_label, fontsize=14)
        self.ax.set_ylabel(y_label, fontsize=14)
        self.ax.set_title(title, fontsize=16)

        canvas = FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        # Convert Matplotlib surface to Pygame surface
        graph_surface = pygame.image.fromstring(raw_data, size, "RGB")

        # Blit the Matplotlib surface onto the Pygame surface
        self.graph_surface.blit(graph_surface, (0, 0))  # for graph appearance
        screen.blit(self.graph_surface, self.graph_surface_rect.topleft)  # Blit the smaller surface onto the main window

    def get_points(self):
        # Calculate the screen coordinates for each data point
        x_step = self.graph_width / max(len(self.data) - 1, 1)
        return [(int(i * x_step), int(self.graph_height - (value / 100.0 * self.graph_height))) for i, value in
                enumerate(self.data)]
