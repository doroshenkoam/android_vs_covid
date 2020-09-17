import pygame

from random import randint

import config as c
import auxiliary as a

# enemy - класс врагов
class enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = a.load_image("virus.png").convert_alpha()
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
        c.WIN.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        if self.rect.x < 0:
            self.points += 1
            self.rect.x = 900 + randint(0, 3000)
        self.rect.x -= self.velocity
        self.counter += 1

        # увеличиваем скорость
        if self.counter == 5 * c.FPS:
            self.velocity += 1
            self.counter = 0

    def get_points(self):
        return self.points

    def start_position(self):
        self.rect.x = 900
        self.velocity = 10
        self.counter = 0
