import pygame as pg
import config as c


class Health:
    def __init__(self, sc, bounds, hp):
        self.sc = sc
        self.bounds = bounds
        self.bottom_x = self.bounds.center[0]
        self.bottom_y = self.bounds.bottom + 20
        self.health = hp
        self.f = pg.font.Font(c.font_name, 12)

        self.sc_text = self.f.render(f'HP: {self.health}', True, c.RED, c.YELLOW)
        self.pos = self.sc_text.get_rect(center=(self.bottom_x, self.bottom_y))

    def draw_health_bar(self):
        if self.health > 0:
            self.sc.blit(self.sc_text, self.pos)
