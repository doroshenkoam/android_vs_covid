import pygame
from random import randint

# инициализируем пакет
pygame.init()
# TODO: вынести в конфиг
FPS = 60
GAME_NAME = "ANDROID VS COVID-19"
WINDOW_SIZE = (800, 600)
DIR = "asset"
WIN = pygame.display.set_mode(WINDOW_SIZE)
runing = True


def game_over():
    global runing
    runing = False


def load_image(file_name):
    file_name = f"{DIR}/{file_name}"
    try:
        image = pygame.image.load(file_name)
    except:
        print(f"Не удалось загрузить изображение: {file_name}")
        raise SystemExit()
    return image


# player - класс основного персонажа
class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y
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
        WIN.blit(self.image, (self.rect.x, self.rect.y))

    def wound(self):
        self.health -= 1
        print(self.health)
        if self.health <= 0:
            game_over()


class enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("virus.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        self.counter = 0

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        if self.rect.x < 0:
            self.rect.x = 900 + randint(0, 1000)
        self.rect.x -= self.velocity
        self.counter += 1

        # увеличиваем скорость
        if self.counter == 10 * FPS:
            self.velocity += 1
            self.counter = 0


def re_draw_window(man, viruses):
    WIN.blit(BG, (0, 0))
    man.draw()
    # viruses.draw(BG)
    for virus in viruses:
        virus.draw()
    pygame.display.update()


def main():
    global BG
    global runing

    # настройки окна
    pygame.display.set_caption(GAME_NAME)
    BG = load_image("imgonline-com-ua-Resize-D1KIqVCWF3.jpg")

    clock = pygame.time.Clock()

    # игровой персонаж
    man = player((800 - 130) / 2, 375, 110, 130)
    # враги
    viruses = pygame.sprite.Group()
    viruses.add(enemy(900, 375, 150, 150, viruses))

    # основной цикл
    while runing:

        clock.tick(FPS)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                runing = False

        # враги
        for virus in viruses:
            virus.move()

        # столкновение
        if pygame.sprite.spritecollide(man, viruses, False):
            man.wound()

        # управление
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            runing = False

        # анализ движения
        if keys[pygame.K_LEFT] and man.rect.x > man.velocity:
            man.rect.x -= man.velocity
            man.left = True
            man.right = False
        elif keys[pygame.K_RIGHT] and man.rect.x < 800 - man.width - man.velocity:
            man.rect.x += man.velocity
            man.left = False
            man.right = True
        else:
            man.right = False
            man.left = False
            man.walk_count = 0

        # TODO: баг
        # прыжки
        if not (man.is_jump):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                man.is_jump = True
                man.left = False
                man.right = False
                man.walk_count = 0
        else:
            if man.jump_count >= -10:
                neg = 1
                if man.jump_count < 0:
                    neg = -1
                man.rect.y -= (man.jump_count ** 2) * 0.5 * neg
                man.jump_count -= 1
            else:
                man.is_jump = False
                man.jump_count = 10

        re_draw_window(man, viruses)


if __name__ == "__main__":
    main()