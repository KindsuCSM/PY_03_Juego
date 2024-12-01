import random
import pygame
import sys

from pygame._sprite import Sprite

class Cereza(Sprite):
    def __init__(self, juego):
        super().__init__()
        self.screen = juego.screen

        self.image = pygame.image.load("Recursos/Imagenes/SpritesPowerUp/Items/Cereza.png")
        self.rect = self.image.get_rect()
        self.speed = 3

        self.rect_top = self.rect.top
        self.rect.x = random.randint(20, self.screen.get_width() - self.rect.width - 16)
        self.rect.y = self.speed

    def update(self):
        self.rect.y += self.speed

        if self.rect_top > self.screen.get_height():
            self.kill()

    def draw_cereza(self):
        self.screen.blit(self.image, self.rect)

class Fresita(Sprite):
    def __init__(self, juego):
        super().__init__()
        self.screen = juego.screen

        self.image = pygame.image.load("Recursos/Imagenes/SpritesPowerUp/Items/Fresita.png")
        self.rect = self.image.get_rect()
        self.speed = 4

        self.rect_top = self.rect.top
        self.rect.x = random.randint(20, self.screen.get_width() - self.rect.width - 16)
        self.rect.y = self.speed

    def update(self):
        self.rect.y += self.speed
        if self.rect_top > self.screen.get_height():
            self.kill()

    def draw_fresa(self):
        self.screen.blit(self.image, self.rect)