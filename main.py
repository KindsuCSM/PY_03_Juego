import pygame
from pygame.display import set_mode
from personajes import *

pygame.init()

player = Player(400, 300)
enemies = []

for i in range(5):
    enemy = Enemy(random.randint(0, width - 50), random.randint(10, 500))
    enemies.append(enemy)

running =True

clock = pygame.time.Clock()

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(fondo_redimensionado, background_rect)
    player.draw()
    for enemy in enemies:
        enemy.update_enemy()
        enemy.draw()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Movimiento horizontal izquierda
            player.x -=1
        if keys[pygame.K_d]:  # Movimiento horizontal derecha
            player.x += 1
    pygame.display.flip()
pygame.quit()