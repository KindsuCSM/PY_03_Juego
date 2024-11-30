import pygame
import random
import sys
from pygame._sprite import Sprite

def personaje_aleatorio():
    enemy_images = [
        pygame.image.load("Imagenes/Personajes/Azul.png"),
        pygame.image.load("Imagenes/Personajes/Naranja.png"),
        pygame.image.load("Imagenes/Personajes/Rojo.png"),
        pygame.image.load("Imagenes/Personajes/Rosa.png"),
    ]
    return random.choice(enemy_images)

class Fantasma(Sprite):
    def __init__(self, juego):
        super().__init__()
        self.screen = juego.screen

        self.image = personaje_aleatorio()
        self.rect = self.image.get_rect()
        self.speed = 2
        self.salud = 3

        self.rect_top = self.rect.top
        self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)
        self.rect.y = self.speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > self.screen.get_height():
            self.kill()

    def recibir_danio(self, danio):
        self.salud -= danio
        if self.salud <= 0:
            self.kill()
            return True
        return False

    def draw_fantasma(self):
        self.screen.blit(self.image, self.rect)
