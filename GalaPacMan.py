from string import punctuation

import pygame
import sys

from PowerUp import Fresita, Cereza
from Pantallas import MenuPrincipal, GameOver
from Balas import Bala
from Enemigos import Fantasma, Asteroide
from Jugador import PacMan



class GalaPacMan:

    # Clase de ajustes donde tendremos todas las variables de jugador y enemigo
    def __init__(self):
        pygame.init()
        # Dimensiones de pantalla
        self.screenWidth = 400
        self.screenHeight = 500

        # Fuente pacman
        self.ruta_fuente = "Recursos/UI/Fuentes/retro.ttf"
        self.color_fuente = (250, 250, 153)

        # Configuración de pantalla
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('GalaPacMan')
        self.background = pygame.image.load('Recursos/UI/Background/game_background.png')

        #Fuentes usadas
        self.fuente_pacman = pygame.font.Font(self.ruta_fuente, 30)

        self.pantalla_principal = MenuPrincipal(self)
        self.pantalla_game_over = GameOver(self)

        # Configuración del personaje principal
        self.pacman = PacMan(self)
        self.pacman_group = pygame.sprite.Group()
        self.isVivo = True
        self.isLvl1 = True

        # Configuración para las balas
        self.ancho_bala = 6
        self.alto_bala = 6
        self.color_bala = (250, 250, 153)
        self.balas = pygame.sprite.Group()
        self.bala_espacio = False
        self.ultimo_disparo = 0
        self.retraso_disparo = 100
        self.danio_bala = 1
        self.duracion_tiempo_powerup = 20000  # 20s de powerUp
        self.contador_tiempo_efecto = 0

        # Configuración para los enemigos
        self.fantasmas = pygame.sprite.Group()
        self.nuevo_fantasma = 0
        self.tiempo_entre_fantasmas = 2000

        # Configuración para los asteroides
        self.asteroides = pygame.sprite.Group()
        self.nuevo_asteroide = 0
        self.tiempo_entre_asteroide = 1000

        # Configuración de la puntuación
        self.puntuacion_jugador = 0
        self.vida_pacman = 5
        self.energia_pacman = 0
        self.puntuacion_para_lvl_dos = 300

        # Importar imagenes de Energia
        self.imagenes_energia = {
            0: pygame.image.load("Recursos/SpritesPowerUp/Barra/Incompleta.png"),
            1: pygame.image.load("Recursos/SpritesPowerUp/Barra/Incompleta_1.png"),
            2: pygame.image.load("Recursos/SpritesPowerUp/Barra/Incompleta_2.png"),
            3: pygame.image.load("Recursos/SpritesPowerUp/Barra/Incompleta_3.png"),
            4: pygame.image.load("Recursos/SpritesPowerUp/Barra/Incompleta_4.png"),
            5: pygame.image.load("Recursos/SpritesPowerUp/Barra/Completa.png"),
            6: pygame.image.load("Recursos/SpritesPowerUp/Barra/PowerUpActivado.png")
        }
        self.pacman_isPowerUp = False
        self.power_up_activado = False
        self.crear_power_up = True

        # Importar imagenes de UI
        self.corazon_lleno = pygame.image.load("Recursos/ItemVida/CorazonLleno.png")
        self.corazon_vacio = pygame.image.load("Recursos/ItemVida/CorazonVacio.png")

        self.power_ups_cerezas = pygame.sprite.Group()
        self.power_ups_fresas = pygame.sprite.Group()

        self.nuevo_power_up_cerezas = 0
        self.nuevo_power_up_fresas = 0

        self.tiempo_entre_fresitas = 32000
        self.tiempo_entre_cereza = 10000


    def bucle_juego(self):
        mostrar_inicio = True
        run = True

        clock = pygame.time.Clock()
        while run:
            if mostrar_inicio:
                self.pantalla_principal.draw_pantalla_principal()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pantalla_principal.btn_start_rect.collidepoint(event.pos):
                            mostrar_inicio = False
                        if self.pantalla_principal.btn_nivel_uno_rect.collidepoint(event.pos):
                            mostrar_inicio = False
                            self.isLvl1 = True
                        if self.pantalla_principal.btn_nivel_dos_rect.collidepoint(event.pos):
                            mostrar_inicio = False
                            self.isLvl1 = False
                            self.puntuacion_jugador = 300
                        if self.pantalla_principal.btn_exit_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
            else:
                if self.puntuacion_jugador < self.puntuacion_para_lvl_dos:
                    self.isLvl1 = True
                else:
                    self.isLvl1 = False
                clock.tick(60)
                if self.isVivo:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_e:
                                self.power_up_activado = True
                                self.pacman.cambiar_sprite(abierto=False, powerup=self.pacman_isPowerUp)
                            if event.key == pygame.K_SPACE:
                                self.pacman.cambiar_sprite(abierto=True, powerup=self.pacman_isPowerUp)
                                self.crear_bala()
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_SPACE:
                                self.pacman.cambiar_sprite(abierto=False, powerup=self.pacman_isPowerUp)
                            if event.key == pygame.K_e:
                                self.power_up_activado = False
                                self.pacman.cambiar_sprite(abierto=False, powerup=self.pacman_isPowerUp)
                    keys = pygame.key.get_pressed()
                    self.pacman.mover(keys, powerUp=self.pacman_isPowerUp)
                    self.screen.blit(self.background, (0, 0))
                    # Función para actualizar los eventos de la pantalla
                    self.actualizar_pantalla()
                    pygame.display.flip()
                if not self.isVivo:
                    self.pantalla_game_over.draw_pantalla_game_over()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.pantalla_game_over.btn_retry_rect.collidepoint(event.pos) and not self.isVivo:
                                self.restablecer_parametros()

                pygame.display.flip()

    def restablecer_parametros(self):
        self.isVivo = True
        self.vida_pacman = 5
        self.energia_pacman = 0
        self.puntuacion_jugador = 0
        self.fantasmas = pygame.sprite.Group()
        self.power_ups_fresas = pygame.sprite.Group()
        self.power_ups_cerezas = pygame.sprite.Group()
        self.asteroides = pygame.sprite.Group()

    def actualizar_pantalla(self):
        self.pacman.draw_pacman()  # Dibujar a PacMan en pantalla
        # Actualizar posiciones
        self.balas.update()
        self.fantasmas.update()
        self.power_ups_cerezas.update()
        self.power_ups_fresas.update()

        # Crear enemigos y powerUps
        if not self.isLvl1:
            self.asteroides.update()
            self.crear_asteroides()
            self.colision_asteroides()
            for asteroide in self.asteroides.sprites():
                asteroide.draw_asteroide()

        self.crear_enemigos()

        if self.crear_power_up:
            self.crear_power_up_fresa()
            self.crear_power_up_cereza()

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
        self.pantalla_puntuacion()
        self.pantalla_vida_jugador()
        self.funcion_power_up()

    def crear_bala(self):
        tiempo_actual = pygame.time.get_ticks()
        n_bala = Bala(self)
        if tiempo_actual - self.ultimo_disparo >= self.retraso_disparo:
            self.balas.add(n_bala)
            self.ultimo_disparo = tiempo_actual

    def crear_enemigos(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nuevo_fantasma >= self.tiempo_entre_fantasmas:
            n_fantasma = Fantasma(self)
            self.fantasmas.add(n_fantasma)
            self.nuevo_fantasma = tiempo_actual

    def crear_asteroides(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nuevo_asteroide >= self.tiempo_entre_asteroide:
            n_asteroide = Asteroide(self)
            self.asteroides.add(n_asteroide)
            self.nuevo_asteroide = tiempo_actual

    def crear_power_up_fresa(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nuevo_power_up_fresas >= self.tiempo_entre_fresitas:
            n_fresita = Fresita(self)
            self.power_ups_fresas.add(n_fresita)
            self.nuevo_power_up_fresas = tiempo_actual

    def crear_power_up_cereza(self):
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
                    self.puntuacion_jugador += 10

    def colision_fantasma(self):
        for fantasma in self.fantasmas:
            if fantasma.rect.top >= self.screen.get_height():
                fantasma.kill()
                self.vida_pacman -= 1
        if self.vida_pacman <= 0:
            self.isVivo = False

    def colision_asteroides(self):
        self.pacman_group.add(self.pacman)
        colision_balas_asteroides = pygame.sprite.groupcollide(self.balas, self.asteroides, True, False)
        for asteroides in colision_balas_asteroides.values():
            for asteroide in asteroides:
                if asteroide.recibir_danio(self.danio_bala):
                    self.puntuacion_jugador += 100

        colision_pacman = pygame.sprite.groupcollide(self.asteroides, self.pacman_group, True, False)
        if len(colision_pacman)  > 0:
            self.vida_pacman -= 2


    def colision_power_ups(self):
        self.pacman_group.add(self.pacman)
        colision_cerezas = pygame.sprite.groupcollide(self.power_ups_cerezas, self.pacman_group, True, True)
        colision_fresas = pygame.sprite.groupcollide(self.power_ups_fresas, self.pacman_group, True, True)

        if self.energia_pacman > 5:
            self.energia_pacman = 5

        if len(colision_cerezas) != 0:
            self.energia_pacman += 1
        if len(colision_fresas) != 0:
            self.energia_pacman += 2

    def activar_power_up(self, tiempo_actual):
        if self.energia_pacman >= 5 and self.power_up_activado and not self.pacman_isPowerUp:
            self.pacman_isPowerUp = True
            self.danio_bala = 3
            self.color_bala = (250, 0, 0)
            self.crear_power_up = False
            self.contador_tiempo_efecto = tiempo_actual
            self.power_up_activado = False

    def desactivar_power_up(self, tiempo_actual):
        if self.pacman_isPowerUp and tiempo_actual - self.contador_tiempo_efecto >= self.duracion_tiempo_powerup:
            self.pacman.cambiar_sprite(abierto=False, powerup=self.pacman_isPowerUp)
            self.energia_pacman = 0
            self.pacman_isPowerUp = False
            self.danio_bala = 1
            self.color_bala = (250, 250, 153)
            self.crear_power_up = True
            self.contador_tiempo_efecto = 0

    def funcion_power_up(self):
        tiempo_actual = pygame.time.get_ticks()
        self.colision_power_ups()
        self.pantalla_barra_energia()
        self.activar_power_up(tiempo_actual)
        self.desactivar_power_up(tiempo_actual)

    def pantalla_vida_jugador(self):
        for i in range(self.vida_pacman):
            self.screen.blit(self.corazon_vacio, (25 + i * 25, 10))
        for i in range(self.vida_pacman):
            if self.vida_pacman >= (i + 1):
                self.screen.blit(self.corazon_lleno, (25 + i * 25, 10))

    def pantalla_puntuacion(self):
        superficie_texto = self.fuente_pacman.render(str(self.puntuacion_jugador), True, self.color_fuente)
        rect_texto = superficie_texto.get_rect()
        rect_texto.topright = (380, 10)
        self.screen.blit(superficie_texto, rect_texto)

    def pantalla_barra_energia(self):
        if self.pacman_isPowerUp:
            self.refactorizar_imagenes_energia(self.imagenes_energia[6])
        else:
            self.refactorizar_imagenes_energia(self.imagenes_energia[self.energia_pacman])

    def refactorizar_imagenes_energia(self, archivo):
        imagen = pygame.transform.scale(archivo, (136, 30))
        self.screen.blit(imagen, (20, 50))

if __name__ == '__main__':
    a = GalaPacMan()
    a.bucle_juego()
