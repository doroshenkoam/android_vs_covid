import pygame

from time import sleep
from random import randint

# инициализируем пакет
pygame.init()
pygame.font.init()
# TODO: вынести в конфиг
FPS = 60
GAME_NAME = "ANDROID VS COVID-19"
WINDOW_SIZE = (800, 600)
DIR = "asset"
WIN = pygame.display.set_mode(WINDOW_SIZE)
runing = True
intro = True

# game_intro - меню
def game_intro(font):
    global intro
    global runing

    img = load_image("game_intro.jpg")

    while intro:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                intro = False
                runing = False
                break

        # управление
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            intro = False
            runing = False
            break

        if keys[pygame.K_KP_ENTER]:
            intro = False
            sleep(1)
            break

        WIN.blit(img, (0, 0))
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
        WIN.blit(text1, (50, 100))
        WIN.blit(text2, (50, 200))
        WIN.blit(text3, (50, 300))
        pygame.display.update()


# game_over - конец игры, проиграли
def game_over(intro_font, point, viruses):
    global runing
    global intro
    intro = True
    runing = True
    WIN.blit(load_image("game_over.jpg"), (0, 0))
    pygame.display.flip()
    sleep(3)

    # обновляем счетчик и хп
    point.count = 0
    for virus in viruses:
        virus.points = 0
        virus.start_position()

    game_intro(intro_font)


def load_image(file_name):
    file_name = f"{DIR}/{file_name}"
    try:
        image = pygame.image.load(file_name)
    except:
        print(f"Не удалось загрузить изображение: {file_name}")
        raise SystemExit()
    return image


# points - класс очки
class points:
    def __init__(self, font):
        self.count = 0
        self.font = font

    def draw(self):
        text = self.font.render(f"Points: {self.count}", 1, (180, 0, 0))
        WIN.blit(text, (10, 10))

    def up(self, point):
        self.count = point


# player - класс основного персонажа
class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, font_health):
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
        self.jump_count = 9
        self.health = 100
        self.font_health = font_health

    def draw(self):
        # MAN 110x130*32
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        text = self.font_health.render(f"Health: {self.health}", 1, (180, 0, 0))
        WIN.blit(text, (400, 10))

    def wound(self):
        self.health -= 1

    def kill(self, intro_font, point, viruses):
        if self.health <= 0:
            self.health = 100
            game_over(intro_font, point, viruses)


# enemy - класс врагов
class enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("virus.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)
        self.rect.x = x
        self.rect.y = y
        self.width = width - 50
        self.height = height - 50
        self.velocity = 10
        self.counter = 0
        self.points = 0

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        if self.rect.x < 0:
            self.points += 1
            self.rect.x = 900 + randint(0, 1000)
        self.rect.x -= self.velocity
        self.counter += 1

        # увеличиваем скорость
        if self.counter == 10 * FPS:
            self.velocity += 1
            self.counter = 0

    def get_points(self):
        return self.points

    def start_position(self):
        self.rect.x = 900
        self.velocity = 10
        self.counter = 0


def re_draw_window(man, point, viruses):
    WIN.blit(BG, (0, 0))
    point.draw()
    man.draw()
    for virus in viruses:
        virus.draw()
    pygame.display.update()


def main():
    global BG
    global runing

    # тикер отрисовки кадров
    clock = pygame.time.Clock()
    # настройки окна
    pygame.display.set_caption(GAME_NAME)

    # игровое меню
    intro_font = pygame.font.Font(None, 72)
    game_intro(intro_font)

    BG = load_image("bg.jpg")

    # очки
    points_font = pygame.font.Font(None, 36)
    point = points(points_font)
    # игровой персонаж
    health_font = pygame.font.Font(None, 72)
    man = player((800 - 130) / 2, 375, 110, 130, health_font)
    # враги
    viruses = pygame.sprite.Group()
    viruses.add(enemy(900, 390, 150, 150, viruses))

    # основной цикл
    while runing:

        clock.tick(FPS)

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
            runing = False
            break

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

        # прыжки
        if not (man.is_jump):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                man.is_jump = True
                man.left = False
                man.right = False
                man.walk_count = 0
        else:
            if man.jump_count >= -9:
                neg = 1
                if man.jump_count < 0:
                    neg = -1
                man.rect.y -= (man.jump_count ** 2) * neg
                man.jump_count -= 1
            else:
                man.is_jump = False
                man.jump_count = 9

        re_draw_window(man, point, viruses)

        # если перса убили, конец игры
        man.kill(intro_font, point, viruses)


if __name__ == "__main__":
    main()