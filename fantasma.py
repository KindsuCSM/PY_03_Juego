from random import random

import pygame
import sys

class Fantasma:
    def __init__(self, juego):
        self.screen = juego.screen
        self.screen_rect = juego.screen.get_rect()
        self.image = self.personajeAleatorio()
        self.rect = self.image.get_rect()

    def personajeAleatorio(self):
        enemy_images = [
            pygame.image.load("Personajes/Azul.png"),
            pygame.image.load("Personajes/Naranja.png"),
            pygame.image.load("Personajes/Rojo.png"),
            pygame.image.load("Personajes/Rosa.png"),
        ]
        return random.choice(enemy_images)
