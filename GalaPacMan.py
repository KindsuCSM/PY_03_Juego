import pygame
import sys

import fantasma
from ItemsPowerUp import Fresita, Cereza
from bala_peq import Bala
from fantasma import Fantasma
from pacman import PacMan


class GalaPacMan:

    # Clase de ajustes donde tendremos todas las variables de jugador y enemigo
    def __init__(self):
        # Dimensiones de pantalla
        self.screenWidth = 400
        self.screenHeight = 500

        # Fuente pacman
        self.ruta_fuente = "Recursos/UI/retro.ttf"
        self.color_fuente = (250, 250, 153)

        # Inicialización de pygame
        pygame.init()
        # Configuración de pantalla
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('GalaPacMan')
        self.background = pygame.image.load('Recursos/UI/game_background.png')

        # Configuración del personaje principal
        self.pacman = PacMan(self)
        self.vida_pacman = 5
        self.energia_pacman = 4

        # Configuración para las balas
        self.ancho_bala = 6
        self.alto_bala = 6
        self.color_bala = (250, 250, 153)
        self.balas = pygame.sprite.Group()
        self.bala_espacio = False
        self.ultimo_disparo = 0
        self.retraso_disparo = 100
        self.danio_bala = 1
        self.duracion_tiempo_powerup = 20000 #20s de powerUp
        self.contador_tiempo_efecto = 0

        # Configuración para los enemigos
        self.fantasmas = pygame.sprite.Group()
        self.nuevo_fantasma = 0
        self.tiempo_entre_fantasmas = 3000

        # Configuración de la puntuación
        self.puntuacionJugador = 0

        # Importar imagenes de Energia
        self.imagenes_energia = {
            0: pygame.image.load("Recursos/ItemEnergia/Incompleta.png"),
            1: pygame.image.load("Recursos/ItemEnergia/Incompleta_1.png"),
            2: pygame.image.load("Recursos/ItemEnergia/Incompleta_2.png"),
            3: pygame.image.load("Recursos/ItemEnergia/Incompleta_3.png"),
            4: pygame.image.load("Recursos/ItemEnergia/Incompleta_4.png"),
            5: pygame.image.load("Recursos/ItemEnergia/Completa.png")
        }
        self.bool_powerup = False
        self.power_up_activado = False


        # Importar imagenes de UI
        self.corazon_lleno = pygame.image.load("Recursos/ItemVida/CorazonLleno.png")
        self.corazon_vacio = pygame.image.load("Recursos/ItemVida/CorazonVacio.png")

        self.power_ups_cerezas = pygame.sprite.Group()
        self.power_ups_fresas = pygame.sprite.Group()

        self.nuevo_power_up_cerezas = 0
        self.nuevo_power_up_fresas = 0

        self.tiempo_entre_fresitas = 15000
        self.tiempo_entre_cereza = 9000

    def bucle_juego(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.power_up_activado = True
                    if event.key == pygame.K_SPACE:
                        self.pacman.cambiar_sprite(abierto=True, powerup=self.bool_powerup)  # Cambiar la imagen de pacman cuando dispara
                        tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual en milisegundos
                        # Comprobar si ha pasado el tiempo suficiente desde el último disparo
                        if tiempo_actual - self.ultimo_disparo >= self.retraso_disparo:
                            self.crear_bala()
                            self.ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.pacman.cambiar_sprite(abierto=False, powerup=self.bool_powerup) # Cambiar imagen si deja de disparar
                    if event.key == pygame.K_e:
                        self.power_up_activado = False
            keys = pygame.key.get_pressed()
            self.pacman.mover(keys, powerUp=self.bool_powerup)
            self.screen.blit(self.background, (0, 0))

            # Función para actualizar los eventos de la pantalla
            self.actualizar_pantalla()

            pygame.display.flip()

    def actualizar_pantalla(self):
        self.pacman.draw_pacman()  # Dibujar a PacMan en pantalla
        # Actualizar posiciones
        self.balas.update()
        self.fantasmas.update()
        self.power_ups_cerezas.update()
        self.power_ups_fresas.update()

        #Crear enemigos y powerUps
        self.crear_enemigos()
        self.power_up_fresa()
        self.power_up_cereza()

        # Control de colision de bala-enemigo y enemigo-pantalla
        self.colision_bala()
        self.colision_fantasma()

        # Dibujar balas y enemigos en la pantalla
        for bala in self.balas.sprites():
            bala.draw_bala()

        for fantasma_nuevo in self.fantasmas.sprites():
            fantasma_nuevo.draw_fantasma()

        for power_up_cer in self.power_ups_cerezas.sprites():
            power_up_cer.draw_cereza()

        for power_up_fres in self.power_ups_fresas.sprites():
            power_up_fres.draw_fresa()

        # Actualizar puntuacion y vida de PacMan
        self.punctuation()
        self.vida_jugador()
        self.power_up()

    def crear_bala(self):
        n_bala = Bala(self)
        self.balas.add(n_bala)

    def crear_enemigos(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nuevo_fantasma >= self.tiempo_entre_fantasmas:
            n_fantasma = Fantasma(self)
            self.fantasmas.add(n_fantasma)
            self.nuevo_fantasma = tiempo_actual

    def power_up_fresa(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nuevo_power_up_fresas >= self.tiempo_entre_fresitas:
            n_fresita = Fresita(self)
            self.power_ups_fresas.add(n_fresita)
            self.nuevo_power_up_fresas = tiempo_actual

    def power_up_cereza(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nuevo_power_up_cerezas >= self.tiempo_entre_cereza:
            n_cereza = Cereza(self)
            self.power_ups_cerezas.add(n_cereza)
            self.nuevo_power_up_cerezas = tiempo_actual

    def colision_bala(self):
        colision = pygame.sprite.groupcollide(self.balas, self.fantasmas, True, False)
        for fantasmas in colision.values():
            for fantasma in fantasmas:
                if fantasma.recibir_danio(self.danio_bala):
                    self.puntuacionJugador += 10

    def colision_fantasma(self):
        for fantasma in self.fantasmas:
            if fantasma.rect.top >= self.screen.get_height():
                fantasma.kill()
                self.vida_pacman -= 1
        if self.vida_pacman <= 0:
            self.texto_game_over()

    def punctuation(self):
        fuente_pacman = pygame.font.Font(self.ruta_fuente, 30)
        superficie_texto = fuente_pacman.render(str(self.puntuacionJugador), True, self.color_fuente)
        rect_texto = superficie_texto.get_rect()
        rect_texto.topright = (380, 10)
        self.screen.blit(superficie_texto, rect_texto)

    def vida_jugador(self):
        for i in range(5):
            if self.vida_pacman >= (i + 1):
                self.screen.blit(self.corazon_lleno, (25+i*25, 10))

    def power_up(self):
        tiempo_actual = pygame.time.get_ticks()
        pacman_group = pygame.sprite.Group(self.pacman )
        colision_cerezas = pygame.sprite.groupcollide(self.power_ups_cerezas, pacman_group, True, True)
        colision_fresas = pygame.sprite.groupcollide(self.power_ups_fresas, pacman_group, True, True)
        if self.energia_pacman > 5:
            self.energia_pacman = 5

        if len(colision_cerezas) != 0 or len(colision_fresas) != 0:
            self.energia_pacman += 1

        if self.energia_pacman >= 5:
            self.energia_pacman = 5
            if self.power_up_activado and not self.bool_powerup:
                self.bool_powerup = True
                self.danio_bala = 2
                self.contador_tiempo_efecto = tiempo_actual
                self.power_up_activado = False

        if self.bool_powerup and tiempo_actual - self.contador_tiempo_efecto >= self.duracion_tiempo_powerup:
            self.energia_pacman = 0
            self.bool_powerup = False
            self.danio_bala = 1
            self.contador_tiempo_efecto = 0

        self.refactorizar_pintar_energia(self.imagenes_energia[self.energia_pacman])




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

    def refactorizar_pintar_energia(self, archivo):
        imagen = pygame.transform.scale(archivo, (136, 30))
        self.screen.blit(imagen, (20, 50))

if __name__ == '__main__':
    a = GalaPacMan()
    a.bucle_juego()

    #self.tiempo_duracion_powerup = 5000
    #self.tiempo_efecto = 0