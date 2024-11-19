import pygame
from pygame.sprite import Sprite

class Bala(Sprite):
    def __init__(self, juego):
        super().__init__()
        self.screen = juego.screen
        self.color = juego.color_bala
        self.rect = pygame.Rect(0, 0, juego.anchobala, juego.altobala)
        self.rect.midtop = juego.pacman.rect.midtop
        self.y = float(self.rect.y)
        self.velocidad = -5  # Velocidad negativa para que suba

    def update(self):
        # Actualizar posición en Y
        self.y += self.velocidad
        self.rect.y = self.y

        # Eliminar bala si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()

    def draw_bala(self):
        pygame.draw.rect(self.screen, self.color, self.rect)