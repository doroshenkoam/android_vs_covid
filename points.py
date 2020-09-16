import pygame

import config as c

# points - класс очки
class points:
    def __init__(self, font):
        self.count = 0
        self.font = font

    def draw(self):
        text = self.font.render(f"Points: {self.count}", 1, (180, 0, 0))
        c.WIN.blit(text, (10, 10))

    def up(self, point):
        self.count = point
