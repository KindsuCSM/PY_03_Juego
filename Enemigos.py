import pygame
import random
import sys
from pygame._sprite import Sprite



class Fantasma(Sprite):
    def __init__(self, juego):
        super().__init__()
        self.screen = juego.screen

        self.image = self.personaje_aleatorio()
        self.rect = self.image.get_rect()
        self.speed = 2
        self.salud = 3

        self.rect_top = self.rect.top
        self.rect.x = random.randint(20, self.screen.get_width() - self.rect.width - 16)
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

    def personaje_aleatorio(self):
        enemy_images = [
            pygame.image.load("Recursos/Personajes/Enemigos/Fantasmas/Azul.png"),
            pygame.image.load("Recursos/Personajes/Enemigos/Fantasmas/Naranja.png"),
            pygame.image.load("Recursos/Personajes/Enemigos/Fantasmas/Rojo.png"),
            pygame.image.load("Recursos/Personajes/Enemigos/Fantasmas/Rosa.png"),
        ]
        return random.choice(enemy_images)

class Asteroide(Sprite):
    def __init__(self, juego):
        super().__init__()
        self.screen = juego.screen

        self.asteroide = self.asteroide_aleatorio()
        self.rect = self.asteroide.get_rect()
        self.speed = 4
        self.vida_asteroide = 10
        self.rect_top = self.rect.top
        self.rect.x = random.randint(20, self.screen.get_width() - self.rect.width - 16)
        self.rect.y = self.speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen.get_height():
            self.kill()

    def recibir_danio(self, danio):
        self.vida_asteroide -= danio
        if self.vida_asteroide <= 0:
            self.kill()
            return True
        return False

    def draw_asteroide(self):
        self.screen.blit(self.asteroide, self.rect)


    def asteroide_aleatorio(self):
        asteroides_img = [
            pygame.image.load("Recursos/Personajes/Enemigos/Asteroides/Asteroide_corto.png"),
            pygame.image.load("Recursos/Personajes/Enemigos/Asteroides/Asteroide_largo.png")
        ]

        return random.choice(asteroides_img)

