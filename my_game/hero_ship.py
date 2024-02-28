import pygame as pg
from health import Health
import numpy as np

pg.init()
from PIL import Image, ImageFilter


class Ship(Health):
    def __init__(self, sc, hp, accel_x=0):
        self.sc = sc
        self.file_name = 'game_icons/ship.png'
        self.img = self.convert_PIL_to_sc(self.file_name, 15)

        self.sc_rect = sc.get_rect()
        self.hero_bound = self.img.get_rect(center=self.sc_rect.center)
        self.hp = hp
        self.accel_x = accel_x
        self.max_speed = 6

        self.hero_bound.centerx = float(self.sc_rect.centerx)
        self.hero_bound.centery = float(self.sc_rect.centery)

    @staticmethod
    def convert_PIL_to_sc(file_name, n):
        with Image.open(file_name) as img:
            img.load()

        # another way to decrease the size of image:
        # low_scale_ship1 = pg.transform.scale(self.img, (self.hero_bound.height // 15, self.hero_bound.width // 15))

        low_scale_ship2 = img.resize((img.height // n, img.width // n)).filter(ImageFilter.SHARPEN)
        mode = low_scale_ship2.mode
        size = low_scale_ship2.size
        data = low_scale_ship2.tobytes()

        return pg.image.fromstring(data, size, mode)

    def blitRotate(self, image, pos, originPos, angle):  # поворот около неподвижного центра
        # offset from pivot to center
        image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
        offset_center_to_pivot = pg.math.Vector2(pos) - image_rect.center

        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # rotated image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pg.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        return rotated_image, rotated_image_rect

    @staticmethod
    def angle_between(v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2' """
        v1_u = v1 / np.linalg.norm(v1)
        v2_u = v2 / np.linalg.norm(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def rotate_img(self, img):
        m_pos = pg.mouse.get_pos()
        v1 = np.array([0, -1])
        v2 = np.array([m_pos[0] - self.hero_bound.centerx, m_pos[1] - self.hero_bound.centery])
        angle = self.angle_between(v1, v2) * 180 / np.pi  # in degrees
        if v2[0] > 0:
            angle *= -1
        # sometimes cause some errors (pygame.error: Parameter 'width' is invalid)
        return pg.transform.rotate(img, angle), angle

    def draw(self):
        heroes_health_bar = Health(self.sc, self.hero_bound, self.hp)
        heroes_health_bar.draw_health_bar()

        r = self.blitRotate(self.img, self.hero_bound.center, self.img.get_rect().center, self.rotate_img(self.img)[1])
        rotated_image = r[0]
        rotated_image_rect = r[1]

        self.sc.blit(rotated_image, rotated_image_rect)

        img = self.follow_me()[0]
        img_rect = self.follow_me()[1]
        f = self.blitRotate(img, img_rect.center, img.get_rect().center, self.rotate_img(img)[1])
        self.sc.blit(f[0], f[1])

    # the smooth way to follow
    def follow_me(self, fpos=(270, 170)):
        LERP_FACTOR = 0.05
        minimum_distance = 35
        maximum_distance = 65
        # fpos = self.hero_bound.topleft
        img = pg.image.load('game_icons/rocket.png')
        img = pg.transform.scale(img, (img.get_width()//15, img.get_height()//15))
        target_vector = pg.math.Vector2(self.hero_bound.center)
        follower_vector = pg.math.Vector2(*fpos)
        new_follower_vector = pg.math.Vector2(*fpos)

        distance = follower_vector.distance_to(target_vector)
        if distance > minimum_distance:
            direction_vector = (target_vector - follower_vector) / distance
            min_step = max(0, int(distance - maximum_distance))
            max_step = distance - minimum_distance
            step_distance = min_step + (max_step - min_step) * LERP_FACTOR
            new_follower_vector = follower_vector + direction_vector * step_distance

        # return new_follower_vector.x, new_follower_vector.y
        img_rect = img.get_rect(center=new_follower_vector)
        return img, img_rect
