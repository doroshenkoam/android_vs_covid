import pygame

from time import sleep

import config as c

# load_image - загрузка изображения на спрайт
def load_image(file_name):
    file_name = f"{c.DIR}/{file_name}"
    try:
        image = pygame.image.load(file_name)
    except:
        print(f"Не удалось загрузить изображение: {file_name}")
        raise SystemExit()
    return image


# game_over - конец игры, проиграли
def game_over(intro_font, point, viruses):
    c.intro = True
    c.runing = True
    c.WIN.blit(load_image("game_over.jpg"), (0, 0))
    draw_final_points(point)
    pygame.display.flip()
    sleep(5)

    # обновляем счетчик и хп
    point.count = 0
    for virus in viruses:
        virus.points = 0
        virus.start_position()

    game_intro(intro_font)


# game_intro - меню
def game_intro(font):
    img = load_image("game_intro.jpg")

    while c.intro:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                c.intro = False
                c.runing = False
                break

        # управление
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            c.intro = False
            c.runing = False
            break

        if keys[pygame.K_KP_ENTER]:
            c.intro = False
            sleep(1)
            break

        c.WIN.blit(img, (0, 0))
        text1 = font.render(
            "ANDROID VS COVID-19",
            1,
            (180, 0, 0),
        )
        text2 = font.render(
            "Press Enter to start game",
            1,
            (180, 0, 0),
        )
        text3 = font.render(
            "Press Esq to quit",
            1,
            (180, 0, 0),
        )
        c.WIN.blit(text1, (50, 100))
        c.WIN.blit(text2, (50, 200))
        c.WIN.blit(text3, (50, 300))
        pygame.display.update()


# re_draw_window - перерисовка основного окна
def re_draw_window(BG, man, point, viruses):
    c.WIN.blit(BG, (0, 0))
    point.draw()
    man.draw()
    for virus in viruses:
        virus.draw()
    pygame.display.update()


def draw_final_points(point):
    font = pygame.font.Font(None, 110)
    text = font.render(
        f"YOU POINTS: {point.get()}",
        1,
        (50, 205, 50),
    )
    c.WIN.blit(text, (100, 200))
