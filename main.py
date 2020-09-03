import pygame

# инициализируем пакет
pygame.init()
# TODO: вынести в конфиг
FPS = 60
GAME_NAME = "SURVIVAL"
WINDOW_SIZE = (1024, 720)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def object_draw(sc):
    pygame.draw.rect(sc, RED, (50, 50, 50, 75))


def main():
    # настройки окна
    # TODO: вынести в конфиг
    sc = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(GAME_NAME)

    clock = pygame.time.Clock()

    # отрисовываем объект
    object_draw(sc)

    # основной цикл
    while True:

        clock.tick(FPS)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return

        pygame.display.update()


if __name__ == "__main__":
    main()