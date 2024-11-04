import random
import pygame

# Initialize pygame and screen parameters
pygame.init()
width = 800
height = 600
fps = 60

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jueguito")

# Load the background image
background_image = pygame.image.load("background/background_layer_1.png").convert()
fondo_redimensionado = pygame.transform.scale(background_image, (width, height)) # Redimensionar
background_rect = fondo_redimensionado.get_rect()

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 60
        self.velocity = 5
        self.image = pygame.image.load("background/player.png").convert_alpha()  # Use convert_alpha for transparency

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 50
        self.velocity = 2
        self.direction = 1
        self.image = pygame.image.load("background/enemy.png").convert_alpha()

    def update_enemy(self):
        self.x += self.velocity * self.direction
        if self.x < 0 or self.x + self.width > width:
            self.direction *= -1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
