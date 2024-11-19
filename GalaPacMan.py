import pygame
import sys
from bala_peq import Bala
from pacman import PacMan

class GalaPacMan:
    def __init__(self):
        self.screenWidth = 400
        self.screenHeight = 300

        pygame.init()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('GalaPacMan')
        self.color = (0, 0, 0)
        self.anchobala = 3
        self.altobala = 15
        self.color_bala = (250, 250, 250)
        self.pacman = PacMan(self)
        self.balas = pygame.sprite.Group()

        self.bala_espacio = False
        self.ultimo_disparo = 0
        self.retraso_disparo = 100

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
                            self.disparar()
                            self.ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo

            keys = pygame.key.get_pressed()
            self.pacman.mover(keys)

            # Actualizar balas
            self.balas.update()

            # Dibujar elementos
            self.screen.fill(self.color)
            self.pacman.dibujar()
            for bala in self.balas.sprites():
                bala.draw_bala()
            pygame.display.flip()

    def disparar(self):
        n_bala = Bala(self)
        self.balas.add(n_bala)


if __name__ == '__main__':
    a = GalaPacMan()
    a.bucle_juego()