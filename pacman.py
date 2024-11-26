import pygame
import sys

class PacMan:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image_cerrado = pygame.image.load('Personajes/PacManCerrado.png')
        self.image_abierto = pygame.image.load('Personajes/PacManAbierto.png')
        self.image = self.image_cerrado
        self.rect = self.image_cerrado.get_rect()
        self.rect.midbottom = game.screen.get_rect().midbottom  # Inicializa en el centro inferior
        self.speed = 3

    def mover(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.rect.left < 0:  # Si se pasa del límite izquierdo
                self.rect.left = 0
        if keys[pygame.K_d]:  # Mover a la derecha
            self.rect.x += self.speed
            if self.rect.right > self.screen_rect.right:
                self.rect.right = self.screen_rect.right

    def draw_pacman(self):
        self.screen.blit(self.image, self.rect)

    def cambiar_sprite (self, abierto = True):
        if abierto:
            self.image = self.image_abierto
        else:
            self.image = self.image_cerrado

