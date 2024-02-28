import pygame as pg
import config as c
from random import randint
from bullets import bullets
from health import Health


enemies_data = ({'file_name': 'game_icons/alien (1).png', 'hp_minus': 5},
                {'file_name': 'game_icons/alien.png', 'hp_minus': 10},
                {'file_name': 'game_icons/alien (2).png', 'hp_minus': 15})
# enemies_images = ['game_icons/alien (1).png', 'game_icons/alien.png', 'game_icons/alien (2).png']
loads = [pg.image.load(dict_en['file_name']) for dict_en in enemies_data]
enemies_surf = [pg.transform.scale(img, (img.get_height() // 10, img.get_width() // 10)) for img in loads]
enemies = pg.sprite.Group()


def create_enemies(ship, group):
    indx = randint(0, len(loads) - 1)
    speed = 2
    hp_minus = enemies_data[indx]['hp_minus']

    p = randint(0, 2079)
    pos_en = (0, 0)  # просто так
    if p < 420:
        pos_en = (-10, p - 10)
    elif p < 1040:
        pos_en = (p - 420 - 10, 410)
    elif p < 1460:
        pos_en = (610, 410 - (p - 1040))
    elif p < 2079:
        pos_en = (610 - (p - 1460), -10)

    return Enemies(ship, speed, enemies_surf[indx], group, pos_en, hp_minus)


def collide_enemies(score, ship, hp):
    for enemy in enemies:
        for bullet in bullets:
            if bullet.rect.colliderect(enemy.rect):
                score += 1
                c.d.play()
                enemy.kill()
                bullet.kill()
        if ship.hero_bound.colliderect(enemy.rect):
            c.d.play()
            ship.hp -= enemy.hp_minus
            enemy.kill()

    return score


class Enemies(pg.sprite.Sprite, Health):
    def __init__(self, ship, speed, surf, group, pos_en, hp_minus):
        pg.sprite.Sprite.__init__(self)
        self.sc = ship.sc
        self.sc_rect = self.sc.get_rect()
        # self.theta = -ship.rotate_img(ship.img)[1] * np.pi / 180  # в радианах
        self.ship = ship
        self.ship_rect = ship.hero_bound

        # обязательны
        # графическое представление спрайта (ссылка на Surface)
        self.image = surf
        # положение и размер спрайта
        self.rect = self.image.get_rect(center=pos_en)
        self.speed = speed
        self.hp_minus = hp_minus

        self.surface = pg.Surface((640, 440))
        self.surface_rect = self.surface.get_rect(topleft=(-10, -10))

        self.add(group)

    def update(self):
        if self.surface_rect.collidepoint(self.rect.center):
            pos_sh = self.ship.hero_bound.center
            pos = pg.Vector2(pos_sh)
            move = pos - pg.Vector2(self.rect.center)
            move.normalize_ip()
            move *= self.speed
            self.rect.center += move
        else:
            self.kill()

    def draw_health(self):
        enemies_health_bar = Health(self.sc, self.rect, self.hp_minus)
        enemies_health_bar.draw_health_bar()
