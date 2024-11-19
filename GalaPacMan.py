import pygame
import sys

import fantasma
from bala_peq import Bala
from fantasma import Fantasma
from pacman import PacMan

class GalaPacMan:
    def __init__(self):
        self.screenWidth = 400
        self.screenHeight = 500

        pygame.init()
        #Creamos las variables para la pantalla
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('GalaPacMan')
        self.color = (0, 0, 0)

        #Creamos la variable del personaje principal
        self.pacman = PacMan(self)

        #Creamos las variables necesarias para las balas
        self.ancho_bala = 3
        self.alto_bala = 15
        self.color_bala =  (250, 250, 250)
        self.balas = pygame.sprite.Group()
        self.bala_espacio = False
        self.ultimo_disparo = 0
        self.retraso_disparo = 100

        #Creamos las variables necesarias para los enemigos
        self.fantasmas = pygame.sprite.Group()
        self.nuevo_fantasma = 0
        self.tiempo_entre_fantasma = 3000

    def bucle_juego(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual en milisegundos

                        # Comprobar si ha pasado el tiempo suficiente desde el último disparo
                        if tiempo_actual - self.ultimo_disparo >= self.retraso_disparo:
                            self.crear_bala()
                            self.ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo

            keys = pygame.key.get_pressed()
            self.pacman.mover(keys)

            # Actualizar balas
            self.balas.update()
            self.fantasmas.update()
            self.crear_enemigos()



            self.screen.fill(self.color)
            #Creacion de pacman y balas
            self.pacman.draw_pacman()
            #Crear balas y fantasmas
            for bala in self.balas.sprites():
                bala.draw_bala()
            for fantasma_nuevo in self.fantasmas.sprites():
                fantasma_nuevo.draw_fantasma()
            pygame.display.flip()

    def crear_bala(self):
        n_bala = Bala(self)
        self.balas.add(n_bala)

    def crear_enemigos(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nuevo_fantasma >= self.tiempo_entre_fantasma:
            n_fantasma = Fantasma(self)
            self.fantasmas.add(n_fantasma)
            self.nuevo_fantasma = tiempo_actual

if __name__ == '__main__':
    a = GalaPacMan()
    a.bucle_juego()