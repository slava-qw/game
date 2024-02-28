import pygame as pg
import control_events
import config as c
from hero_ship import Ship
from bullets import bullets
from enemies import enemies, collide_enemies


def main():
    pg.init()

    sc = pg.display.set_mode((c.W, c.H))  # don't change the screen
    pg.display.set_caption("Werlon")
    pg.display.set_icon(pg.image.load('game_icons\\free-icon-infinite-7588497.png'))

    pg.mixer.music.load('music/background.mp3')
    pg.mixer.music.play(-1)

    clock = pg.time.Clock()

    sc.fill(c.PURPLE_DARK)
    ship = Ship(sc, c.hp)

    # lstsq_vec = pg.font.Font('fonts/Comfortaa-VariableFont_wght.ttf', 80)
    # b = pg.mixer.Sound("music/bullets.mp3")
    # d = pg.mixer.Sound("music/death.mp3")

    pg.time.set_timer(pg.USEREVENT, 1000)

    pg.mouse.set_visible(False)
    while True:
        clock.tick(c.FPS)
        if not c.restart_game and c.start_game:

            sc_text = c.f.render(f'Score: {c.score}', True, c.PURPLE, None)

            control_events.update_screen(c.PURPLE_DARK, sc, ship, sc_text)

        control_events.control(ship, c.speed, sc)

        pos_for_m = pg.mouse.get_pos()
        mouse_img = pg.image.load('game_icons\\target.png')
        mouse_img = pg.transform.scale(mouse_img, (mouse_img.get_width() // 30, mouse_img.get_height() // 30))

        if pg.mouse.get_focused() and ship.hp > 0:

            enemies.draw(sc)
            # show the enemies' health bar
            # for enemy in enemies:
            #     enemy.draw_health()
            bullets.draw(sc)

            sc.blit(mouse_img, (pos_for_m[0] - mouse_img.get_width()//2, pos_for_m[1] - mouse_img.get_height()//2))

            pg.display.update()

            bullets.update()
            enemies.update()

            c.score = collide_enemies(c.score, ship, c.hp)

        if not pg.mouse.get_focused() and ship.hp > 0 and c.start_game:
            sc_text = c.f.render(f'Pause', True, c.PURPLE_pause, None)
            pos = sc_text.get_rect(center=sc.get_rect().center)
            sc.fill(c.PURPLE_DARK_pause)
            sc.blit(sc_text, pos)
            ship.draw()

            enemies.draw(sc)
            for enemy in enemies:
                enemy.draw_health()
            bullets.draw(sc)

            pg.display.update()

        if pg.mouse.get_focused() and ship.hp <= 0:
            c.restart_game = True

            control_events.draw_game_over_screen(c.PURPLE_DARK, sc)
            sc.blit(mouse_img, (pos_for_m[0] - mouse_img.get_width() // 2, pos_for_m[1] - mouse_img.get_height() // 2))

            pg.display.update()


if __name__ == '__main__':
    main()
