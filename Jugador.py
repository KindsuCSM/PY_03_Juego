import pygame
import sys
from pygame._sprite import Sprite

class PacMan(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.image_cerrado = pygame.image.load('Recursos/Imagenes/Personajes/Principal/PacManCerrado.png')
        self.image_abierto = pygame.image.load('Recursos/Imagenes/Personajes/Principal/PacManAbierto.png')
        self.image_cerrado_rojo = pygame.image.load('Recursos/Imagenes/Personajes/Principal/PacManCerradoRojo.png')
        self.image_abierto_rojo = pygame.image.load('Recursos/Imagenes/Personajes/Principal/PacManAbiertoRojo.png')
        self.image = self.image_cerrado
        self.rect = self.image_cerrado.get_rect()

        self.rect.midbottom = game.screen.get_rect().midbottom  # Inicializa en el centro inferior
        self.rect.y -= 10
        self.speed = 3
        self.speed_powerup = 4

    def mover(self, keys, powerUp = False):
        if keys[pygame.K_a]:
            if not powerUp:
                self.rect.x -= self.speed
            else:
                self.rect.x -= self.speed_powerup
            if self.rect.left < 20:  # Si se pasa del límite izquierdo
                self.rect.left = 20
        if keys[pygame.K_d]:  # Mover a la derecha
            if not powerUp:
                self.rect.x += self.speed
            else:
                self.rect.x += self.speed_powerup
            if self.rect.right > (self.screen_rect.right - 16):
                self.rect.right = (self.screen_rect.right - 16)

    def draw_pacman(self):
        self.screen.blit(self.image, self.rect)

    def cambiar_sprite (self, abierto = True, powerup = False):
        if abierto:
            if not powerup:
                self.image = self.image_abierto
            else:
                self.image = self.image_abierto_rojo

        else:
            if not powerup:
                self.image = self.image_cerrado
            else:
                self.image = self.image_cerrado_rojo
