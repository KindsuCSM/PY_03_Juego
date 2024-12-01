import pygame
import sys

class MenuPrincipal:
    def __init__(self, juego):
        self.screen = juego.screen

        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()

        self.background_img = pygame.image.load('Recursos/Imagenes/Menu/menu_background.png')
        self.btn_start = pygame.image.load('Recursos/Imagenes/Menu/BotonesPrincipal/menu_start.png')
        self.btn_exit = pygame.image.load('Recursos/Imagenes/Menu/BotonesPrincipal/menu__exit.png')
        self.btn_nivel_uno = pygame.image.load('Recursos/Imagenes/Menu/BotonesPrincipal/menu_lvl1.png')
        self.btn_nivel_dos = pygame.image.load('Recursos/Imagenes/Menu/BotonesPrincipal/menu_lvl2.png')

        self.btn_start_rect = self.btn_start.get_rect(center=(self.screenWidth / 2, self.screenHeight / 2))
        self.btn_nivel_uno_rect = self.btn_nivel_uno.get_rect(center=(self.screenWidth / 2, self.screenHeight / 2 + 60))
        self.btn_nivel_dos_rect = self.btn_nivel_dos.get_rect(center=(self.screenWidth / 2, self.screenHeight / 2 + 120))
        self.btn_exit_rect = self.btn_exit.get_rect(center=(self.screenWidth / 2, self.screenHeight / 2 + 200))

    def draw_pantalla_principal(self):
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.btn_start, self.btn_start_rect.topleft)
        self.screen.blit(self.btn_nivel_uno, self.btn_nivel_uno_rect.topleft)
        self.screen.blit(self.btn_nivel_dos, self.btn_nivel_dos_rect.topleft)
        self.screen.blit(self.btn_exit, self.btn_exit_rect.topleft)
        pygame.display.update()

class GameOver:
    def __init__(self, juego):
        self.screen = juego.screen
        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()
        self.background_img = pygame.image.load('Recursos/Imagenes/Menu/menu_background.png')

        self.ruta_fuente = "Recursos/Imagenes/UI/Fuentes/retro.ttf"

        self.fuente_game_over = pygame.font.Font(self.ruta_fuente, 60)
        self.btn_retry = pygame.image.load('Recursos/Imagenes/Menu/BotonesGameOver/gameOver_retry.png')
        self.btn_retry_rect = self.btn_retry.get_rect(center=(self.screenWidth / 2, self.screenHeight / 2 + 200))
        self.superficie_texto = self.fuente_game_over.render("Game Over", True, (255, 255, 155))
        self.rect_texto = self.superficie_texto.get_rect()
        self.rect_texto.topleft = (self.screenWidth / 4, self.screenHeight / 2)

    def draw_pantalla_game_over(self):
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.superficie_texto, self.rect_texto)
        self.screen.blit(self.btn_retry, self.btn_retry_rect)