import pygame
from random import randint

# инициализируем пакет
pygame.init()
# TODO: вынести в конфиг
FPS = 60
GAME_NAME = "ANDROID VS COVID-19"
WINDOW_SIZE = (800, 600)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG = pygame.image.load("asset/imgonline-com-ua-Resize-D1KIqVCWF3.jpg")
WIN = pygame.display.set_mode(WINDOW_SIZE)
runing = True


def game_over():
    global runing
    runing = False


# player - класс основного персонажа
class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("asset/player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count = 10
        self.health = 100

    def draw(self):
        # MAN 110x130*32
        WIN.blit(self.image, (self.x, self.y))

    def wound(self):
        self.health -= 10
        print(self.health)
        if self.health <= 0:
            game_over()


class enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("asset/virus.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        self.counter = 0

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))

    def move(self):
        if self.x < 0:
            self.x = 900 + randint(0, 300)
        self.x -= self.velocity
        self.counter += 1

        # увеличиваем скорость
        if self.counter == 10 * FPS:
            self.velocity += 1
            self.counter = 0


def re_draw_window(man, virus):
    WIN.blit(BG, (0, 0))
    man.draw()
    virus.draw()
    pygame.display.update()


def main():
    global runing

    # настройки окна
    pygame.display.set_caption(GAME_NAME)

    clock = pygame.time.Clock()

    # игровой персонаж
    man = player((800 - 130) / 2, 375, 110, 130)
    # враги
    viruses = pygame.sprite.Group()
    virus = enemy(900, 375, 200, 200, viruses)
    viruses.add(virus)

    # основной цикл
    while runing:

        clock.tick(FPS)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                runing = False

        # TODO: не работает
        # враги
        virus.move()
        if pygame.sprite.spritecollide(man, viruses, True):
            man.wound()

        # управление
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

        re_draw_window(man, virus)


if __name__ == "__main__":
    main()