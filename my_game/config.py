import pygame as pg
pg.init()

W = 600
H = 400
speed = 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (239, 228, 176)
RED = (255, 0, 0)
PURPLE = (150, 83, 230)
PURPLE_pause = (130, 103, 162)
PURPLE_DARK = (58, 32, 89)
PURPLE_DARK_pause = (32, 22, 44)
MAGENTA = (255, 0, 255)
MAROON = (176, 48, 96)
MEDIUM_ORCHID = (186, 85, 211)
color_restart = 0
color_exit = 0
color_start = 0

FPS = 120

score = 0
hp = 100

font_name = 'fonts/Comfortaa-VariableFont_wght.ttf'
f = pg.font.Font('fonts/Comfortaa-VariableFont_wght.ttf', 80)

b = pg.mixer.Sound("music/bullets.mp3")
d = pg.mixer.Sound("music/death.mp3")
p_b = pg.mixer.Sound("music/button.mp3")


# automaton of states
game_keep = True
restart_game = False
start_game = False
