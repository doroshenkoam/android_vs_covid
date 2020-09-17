import pygame

import config as c
import player as p
import auxiliary as a
import points as po
import enemy as e

# инициализируем пакет
pygame.init()
pygame.font.init()


def main():
    # тикер отрисовки кадров
    clock = pygame.time.Clock()
    # настройки окна
    pygame.display.set_caption(c.GAME_NAME)

    # игровое меню
    intro_font = pygame.font.Font(None, 72)
    a.game_intro(intro_font)

    BG = a.load_image("bg.jpg")

    # очки
    points_font = pygame.font.Font(None, 36)
    point = po.points(points_font)
    # игровой персонаж
    health_font = pygame.font.Font(None, 72)
    man = p.player((800 - 130) / 2, 375, 70, 70, health_font)
    # враги
    viruses = pygame.sprite.Group()
    viruses.add(e.enemy(900, 390, 150, 150, viruses))

    # основной цикл
    while c.runing:

        clock.tick(c.FPS)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                runing = False
                break

        # враги
        for virus in viruses:
            virus.move()
            point.up(virus.get_points())

        # столкновение
        if pygame.sprite.spritecollide(man, viruses, False):
            man.wound()

        # управление
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            c.runing = False
            break

        # анализ движения
        man.move(keys)

        # прыжки
        man.jump(keys)

        a.re_draw_window(BG, man, point, viruses)

        # если перса убили, конец игры
        man.kill(intro_font, point, viruses)


if __name__ == "__main__":
    main()