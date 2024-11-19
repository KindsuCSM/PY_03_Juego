from pygame.sprite import Sprite

import pygame
import random
import sys




def personaje_aleatorio():
    enemy_images = [
        pygame.image.load("Personajes/Azul.png"),
        pygame.image.load("Personajes/Naranja.png"),
        pygame.image.load("Personajes/Rojo.png"),
        pygame.image.load("Personajes/Rosa.png"),
    ]
    return random.choice(enemy_images)

class Fantasma(Sprite):
    def __init__(self, juego):
        super().__init__()
        self.screen = juego.screen

        self.image = personaje_aleatorio()
        self.rect = self.image.get_rect()
        self.speed = 2

        self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)
        self.rect.y = self.speed



    def update(self):
        self.rect.y += self.speed

        if self.rect.top > self.screen.get_height():
            self.kill()

    def draw_fantasma(self):
        self.screen.blit(self.image, self.rect)
