# inspired by: https://youtu.be/hw_t77lseQs?si=pb5tRP6ae3xJzN5v

from agent import *
from itertools import chain
import numpy as np
import config as cfg
import cv2

import pygame

pygame.init()

window = pygame.display.set_mode((cfg.w, cfg.h))
sc = pygame.Surface((cfg.w, cfg.h), pygame.SRCALPHA)
w2 = window.convert_alpha()

clock = pygame.time.Clock()
run = True
FPS = 60

plane = Plane(w=cfg.w, h=cfg.h)
n = 1000
ag_s = [Agent(
                x=np.random.uniform(0, cfg.w),
                y=np.random.uniform(0, cfg.h),
                v=np.random.uniform(1, 5),
                alpha=np.random.uniform(np.pi / 12, np.pi / 2),
                r=5,
                g=np.random.uniform(np.pi / 12, np.pi / 2),
                surface=window,
                plane=plane
            ) for _ in range(n)]

T_s = [Trail() for _ in range(n)]

for i, Ti in enumerate(T_s):
    Ti.trail.append(ag_s[i])

size = cfg.h, cfg.w

out = cv2.VideoWriter('output3.13_random_sampling.mp4', cv2.VideoWriter_fourcc(*'mp4v'), FPS, (size[1], size[0]), False)

while run:
    m = np.max(plane.m)
    # TODO: make each pixel with particular color depends on the amount of its score
    out.write((plane.m / m * 255).astype(np.uint8))

    window.fill('white')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # make parallel
    for i, Ti in enumerate(T_s):
        draw_all(Ti)

    pygame.display.update()
    clock.tick(FPS)

out.release()
