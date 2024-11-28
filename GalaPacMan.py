import pygame
import sys

import fantasma
from bala_peq import Bala
from fantasma import Fantasma
from pacman import PacMan


class GalaPacMan:

    # Clase de ajustes donde tendremos todas las variables de jugador y enemigo
    def __init__(self):
        # Dimensiones de pantalla
        self.screenWidth = 400
        self.screenHeight = 500
        # Inicialización de pygame
        pygame.init()
        # Configuración de pantalla
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('GalaPacMan')
        self.color = (0, 0, 0)

        # Configuración del personaje principal
        self.pacman = PacMan(self)
        self.hp_pacman = 5

        # Configuración para las balas
        self.ancho_bala = 6
        self.alto_bala = 6
        self.color_bala = (250, 250, 153)
        self.balas = pygame.sprite.Group()
        self.bala_espacio = False
        self.ultimo_disparo = 0
        self.retraso_disparo = 100
        self.danio_bala = 1

        # Configuración para los enemigos
        self.fantasmas = pygame.sprite.Group()
        self.nuevo_fantasma = 0
        self.tiempo_entre_fantasmas = 3000

        # Configuración de la puntuación del jugador
        self.punctuationJugador = 0

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

                        self.pacman.cambiar_sprite(abierto=True) # Cambiar la imagen de pacman cuando dispara

                        # Comprobar si ha pasado el tiempo suficiente desde el último disparo
                        if tiempo_actual - self.ultimo_disparo >= self.retraso_disparo:
                            self.crear_bala()
                            self.ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.pacman.cambiar_sprite(abierto=False) # Cambiar imagen si deja de disparar
            keys = pygame.key.get_pressed()
            self.pacman.mover(keys)
            self.screen.fill(self.color)

            # Función para actualizar los eventos de la pantalla
            self.actualizar_pantalla()

            pygame.display.flip()

    def actualizar_pantalla(self):

        self.pacman.draw_pacman()  # Dibujar a PacMan en pantalla

        # Actualizar posiciones de las balas y los fantasmas
        self.balas.update()
        self.fantasmas.update()

        self.crear_enemigos()  # Crear enemigos aleatorios con un intervalo de 2s

        # Control de colision de bala-enemigo y enemigo-pantalla
        self.colision_bala()
        self.colision_fantasma()

        # Dibujar balas y enemigos en la pantalla
        for bala in self.balas.sprites():
            bala.draw_bala()
        for fantasma_nuevo in self.fantasmas.sprites():
            fantasma_nuevo.draw_fantasma()

        # Actualizar puntuacion y vida de PacMan
        self.punctuation()
        self.texto_vida_jugador()

    def crear_bala(self):
        n_bala = Bala(self)
        self.balas.add(n_bala)

    def crear_enemigos(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nuevo_fantasma >= self.tiempo_entre_fantasmas:
            n_fantasma = Fantasma(self)
            n_fantasma2 = Fantasma(self)
            self.fantasmas.add(n_fantasma)
            self.fantasmas.add(n_fantasma2)
            self.nuevo_fantasma = tiempo_actual

    def colision_bala(self):
        # La vida del fantasma es 1
        # colision = pygame.sprite.groupcollide(self.balas, self.fantasmas, True, True)
        # if len(colision) != 0:
        # self.punctuationJugador += 10

        # La vida del fantasma es 3
        colision = pygame.sprite.groupcollide(self.balas, self.fantasmas, True, False)
        for fantasmas in colision.values():
            for fantasma in fantasmas:
                if fantasma.recibir_danio(self.danio_bala):
                    self.punctuationJugador += 10

    def colision_fantasma(self):
        for fantasma in self.fantasmas:
            if fantasma.rect.top >= self.screen.get_height():
                fantasma.kill()
                self.hp_pacman -= 1
        if self.hp_pacman <= 0:
            self.texto_game_over()

    def punctuation(self):
        fuente = pygame.font.SysFont('Arial', 15)
        superficie_texto = fuente.render("Puntuacion: " + str(self.punctuationJugador), True, (255, 255, 255))
        rect_texto = superficie_texto.get_rect()
        rect_texto.topleft = (20, 20)
        self.screen.blit(superficie_texto, rect_texto)

    def texto_vida_jugador(self):
        fuente = pygame.font.SysFont('Arial', 15)
        superficie_texto = fuente.render("Vida: " + str(self.hp_pacman), True, (255, 255, 255))
        rect_texto = superficie_texto.get_rect()
        rect_texto.topleft = (20, 40)
        self.screen.blit(superficie_texto, rect_texto)

    def texto_game_over(self):
        fuente = pygame.font.SysFont('Arial', 30)
        superficie_texto = fuente.render("Game Over", True, (255, 255, 155))
        rect_texto = superficie_texto.get_rect()
        rect_texto.topleft = (self.screenWidth / 3.4, self.screenHeight / 2)
        self.screen.blit(superficie_texto, rect_texto)
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    a = GalaPacMan()
    a.bucle_juego()
