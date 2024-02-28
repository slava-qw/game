import pygame as pg
import numpy as np

bullets_images = ['game_icons/paintball.png']
loads = [pg.image.load(img) for img in bullets_images]
bullets_surf = [pg.transform.scale(img, (img.get_height()//25, img.get_width()//25)) for img in loads]
bullets = pg.sprite.Group()


def create_bullets(ship, group, pos_m):
    indx = 0
    speed = 5
    pos_sh = ship.hero_bound.center
    return Bullets(ship, speed, bullets_surf[indx], group, pos_m, pos_sh)


class Bullets(pg.sprite.Sprite):
    def __init__(self, ship, speed, surf, group, pos_m, pos_sh):
        pg.sprite.Sprite.__init__(self)
        self.sc = ship.sc
        self.sc_rect = self.sc.get_rect()
        self.theta = -ship.rotate_img(ship.img)[1] * np.pi / 180  # в радианах
        self.ship = ship
        self.ship_rect = ship.hero_bound
        self.image1 = surf
        # обязательны
        # графическое представление спрайта (ссылка на Surface)
        self.image = self.rotate_bullets()[0]
        # self.image = surf
        # положение и размер спрайта
        self.rect = self.image.get_rect(center=self.ship_rect.center)  # не получилось реализовать вылет не из центра (проблемы со знаками theta)
        self.speed = speed

        self.pos_m = pos_m
        self.pos_sh = pos_sh
        self.target = pg.Vector2(self.pos_sh)
        self.pos = pg.Vector2(self.pos_m)

        self.add(group)

    def rotate_bullets(self):
        r = self.ship.blitRotate(self.image1,  self.ship.hero_bound.center, self.image1.get_rect().center, self.ship.rotate_img(self.image1)[1] + 90)
        return r

    def update(self):  # физика движения пули
        if self.sc_rect.collidepoint(self.rect.center):
            # self.rect.centerx += self.speed * np.sin(self.theta)
            # self.rect.centery -= self.speed * np.cos(self.theta)

            move = self.pos - self.target
            move.normalize_ip()
            move *= self.speed
            self.rect.center += move

        else:
            self.kill()
