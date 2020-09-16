import pygame

import config as c
import auxiliary as a

# player - класс основного персонажа
class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, font_health):
        pygame.sprite.Sprite.__init__(self)
        self.image = a.load_image("player.png").convert_alpha()
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
        c.WIN.blit(self.image, (self.rect.x, self.rect.y))
        text = self.font_health.render(f"Health: {self.health}", 1, (180, 0, 0))
        c.WIN.blit(text, (400, 10))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > self.velocity:
            self.rect.x -= self.velocity
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT] and self.rect.x < 800 - self.width - self.velocity:
            self.rect.x += self.velocity
            self.left = False
            self.right = True
        else:
            self.right = False
            self.left = False
            self.walk_count = 0

    def jump(self, keys):
        if not (self.is_jump):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.is_jump = True
                self.left = False
                self.right = False
                self.walk_count = 0
        else:
            if self.jump_count >= -9:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * neg
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 9

    def wound(self):
        self.health -= 1

    def kill(self, intro_font, point, viruses):
        if self.health <= 0:
            self.health = 100
            self.rect.x = (800 - 130) / 2
            self.rect.y = 375
            a.game_over(intro_font, point, viruses)