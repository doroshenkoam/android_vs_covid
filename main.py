import pygame

# инициализируем пакет
pygame.init()
# TODO: вынести в конфиг
FPS = 60
GAME_NAME = "SURVIVAL"
WINDOW_SIZE = (800, 600)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG = pygame.image.load("asset/priroda-nebo-oblaka-svezhest.jpg")
MAN = pygame.image.load("asset/player.png")
WIN = pygame.display.set_mode(WINDOW_SIZE)


# player - класс основного персонажа
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count = 10

    def draw(self):
        # print(MAN)
        # MAN 110x130*32
        WIN.blit(MAN, (self.x, self.y))


def re_draw_window(man):
    WIN.blit(BG, (0, 0))
    man.draw()
    pygame.display.update()


def main():
    # настройки окна
    pygame.display.set_caption(GAME_NAME)

    clock = pygame.time.Clock()

    # основной цикл
    # TODO: вынести в конфиг
    man = player((800 - 130) / 2, 450, 110, 130)
    runinig = True
    while runinig:

        clock.tick(FPS)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                runinig = False

        keys = pygame.key.get_pressed()

        # анализ движения
        if keys[pygame.K_LEFT] and man.x > man.velocity:
            man.x -= man.velocity
            man.left = True
            man.right = False
        elif keys[pygame.K_RIGHT] and man.x < 800 - man.width - man.velocity:
            man.x += man.velocity
            man.left = False
            man.right = True
        else:
            man.right = False
            man.left = False
            man.walk_count = 0

        # прыжки
        if not (man.is_jump):
            if keys[pygame.K_SPACE]:
                man.is_jump = True
                man.left = False
                man.right = False
                man.walk_count = 0
        else:
            if man.jump_count >= -10:
                neg = 1
                if man.jump_count < 0:
                    neg = -1
                man.y -= (man.jump_count ** 2) * 0.5 * neg
                man.jump_count -= 1
            else:
                man.is_jump = False
                man.jump_count = 10

        re_draw_window(man)


if __name__ == "__main__":
    main()