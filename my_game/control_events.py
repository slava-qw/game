import pygame as pg
from bullets import bullets, create_bullets
from enemies import enemies, create_enemies
import config as c


def control(ship, speed, sc):
    if not c.start_game:
        draw_start_screen(sc)
        pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            c.p_b.play()
            exit()

        pos_m = pg.mouse.get_pos()
        keys = pg.key.get_pressed()

        if not c.start_game:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and start_screen(sc)[1][1].collidepoint(pos_m[0], pos_m[1]):
                c.p_b.play()
                c.start_game = True
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and start_screen(sc)[2][1].collidepoint(pos_m[0], pos_m[1]):
                c.p_b.play()
                exit()
        elif pg.mouse.get_focused():
            if (keys[pg.K_a] and not keys[pg.K_d]) and (0 < ship.hero_bound.bottomleft[0]):
                ship.hero_bound.centerx -= speed
            elif (keys[pg.K_d] and not keys[pg.K_a]) and (ship.hero_bound.topright[0] < ship.sc_rect.bottomright[0]):
                ship.hero_bound.centerx += speed
            elif (keys[pg.K_w] and not keys[pg.K_s]) and (0 < ship.hero_bound.topright[1]):
                ship.hero_bound.centery -= speed
            elif (keys[pg.K_s] and not keys[pg.K_w]) and (ship.hero_bound.bottomleft[1] < ship.sc_rect.bottomright[1]):
                ship.hero_bound.centery += speed

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if not c.restart_game:
                    c.b.play()
                create_bullets(ship, bullets, pos_m)
            if event.type == pg.USEREVENT:
                create_enemies(ship, enemies)

            if c.restart_game:
                if game_over_screen(sc)[1][1].collidepoint(pos_m[0], pos_m[1]):
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        c.p_b.play()
                        for enemy in enemies:
                            enemy.kill()
                        for bullet in bullets:
                            bullet.kill()
                        ship.hero_bound.centerx = float(ship.sc_rect.centerx)
                        ship.hero_bound.centery = float(ship.sc_rect.centery)

                        ship.hp = c.hp
                        c.score = 0
                        c.restart_game = False
                if game_over_screen(sc)[3][1].collidepoint(pos_m[0], pos_m[1]) and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    c.p_b.play()
                    exit()


def update_screen(bg_color, sc, ship, sc_text):
    sc.fill(bg_color)
    pos = sc_text.get_rect(center=sc.get_rect().center)
    sc.blit(sc_text, pos)
    # don't increase screen: will be restrictions on movement (sc must change in main loop)
    ship.draw()  # when increase the screen, ship doesn't change its position


def game_over_screen(sc):
    f = pg.font.Font(c.font_name, 80)
    f1 = pg.font.Font(c.font_name, 60)
    f2 = pg.font.Font(c.font_name, 40)

    sc_text = f.render('Game Over', True, c.PURPLE, None)
    sc_text_between = f1.render(f'Your score is {c.score}', True, c.PURPLE, None)
    sc_text_restart = f2.render('Restart', True, c.color_restart, None)
    sc_text_exit = f2.render('Exit', True, c.color_exit, None)

    pos = sc_text.get_rect(center=(sc.get_rect().center[0], sc.get_rect().center[1] * 0.55))
    pos_between = sc_text_between.get_rect(center=(sc.get_rect().center[0], sc.get_rect().center[1]))
    pos_restart = sc_text_restart.get_rect(center=(sc.get_rect().center[0] * 0.5, sc.get_rect().center[1] * 1.65))
    pos_exit = sc_text_exit.get_rect(center=(sc.get_rect().center[0] * 1.5, sc.get_rect().center[1] * 1.65))

    return [[sc_text, pos], [sc_text_restart, pos_restart], [sc_text_between, pos_between], [sc_text_exit, pos_exit]]


def draw_game_over_screen(bg_color, sc):
    c.restart_game = True
    gmo_sc = game_over_screen(sc)

    c.color_restart = c.MEDIUM_ORCHID
    c.color_exit = c.MEDIUM_ORCHID

    sc.fill(bg_color)
    sc.blit(gmo_sc[0][0], gmo_sc[0][1])
    sc.blit(gmo_sc[2][0], gmo_sc[2][1])

    if not gmo_sc[1][1].collidepoint(pg.mouse.get_pos()):
        sc.blit(gmo_sc[1][0], gmo_sc[1][1])
    else:
        c.color_restart = c.MAROON
        sc.blit(gmo_sc[1][0], gmo_sc[1][1])

    if not gmo_sc[3][1].collidepoint(pg.mouse.get_pos()):
        sc.blit(gmo_sc[3][0], gmo_sc[3][1])
    else:
        c.color_exit = c.MAROON
        sc.blit(gmo_sc[3][0], gmo_sc[3][1])


def draw_start_screen(sc):
    sta_sc = start_screen(sc)

    c.color_start = c.MEDIUM_ORCHID
    c.color_exit = c.MEDIUM_ORCHID

    sc.fill(c.PURPLE_DARK)
    sc.blit(sta_sc[0][0], sta_sc[0][1])

    if not sta_sc[1][1].collidepoint(pg.mouse.get_pos()):
        sc.blit(sta_sc[1][0], sta_sc[1][1])
    else:
        c.color_start = c.MAROON
        sc.blit(sta_sc[1][0], sta_sc[1][1])

    if not sta_sc[2][1].collidepoint(pg.mouse.get_pos()):
        sc.blit(sta_sc[2][0], sta_sc[2][1])
    else:
        c.color_exit = c.MAROON
        sc.blit(sta_sc[2][0], sta_sc[2][1])


def start_screen(sc):
    f = pg.font.Font(c.font_name, 80)
    f1 = pg.font.Font(c.font_name, 60)

    sc_text = f.render('Werlon', True, c.PURPLE, None)
    sc_text_start = f1.render('Start', True, c.color_start, None)
    sc_text_exit = f1.render('Exit', True, c.color_exit, None)

    pos = sc_text.get_rect(center=(sc.get_rect().center[0], sc.get_rect().center[1] * 0.75))
    pos_start = sc_text_start.get_rect(center=(sc.get_rect().center[0] * 0.5, sc.get_rect().center[1] * 1.65))

    pos_exit = sc_text_exit.get_rect(center=(sc.get_rect().center[0] * 1.5, sc.get_rect().center[1] * 1.65))

    return [[sc_text, pos], [sc_text_start, pos_start], [sc_text_exit, pos_exit]]
