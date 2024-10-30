import sys, pygame

# Iniciar pygame
pygame.init()

# Declarar e inicializar variables
height = 720 # Altura de ventana
width = 1280 # Ancho de ventana
cian = 0, 255, 255 #Color cian
isJump = False # Inicializar salto en falso
running = True # Inicializar correr en verdadero
salto = 20 #Altura del salto
vel = 5  # Velocidad horizontal
x=0
y=0

posicionInicialAncho = width / 2 #Posicion de personaje en eje Y
posicionInicialAltura = height - 80 #Posicion de personaje en eje X

screen = pygame.display.set_mode((width, height))  # Crear la pantalla
pygame.display.set_caption("Jueguito Python")  # Cambiar el nombre a la ventana
fondo = pygame.image.load("background/background_layer_1.png").convert() #Poner imagen como fondo de la pantalla
fondo_redimensionado = pygame.transform.scale(fondo, (width, height)) # Redimensionar la imagen para que se ajuste al W y H de la ventana
clock = pygame.time.Clock()  # Reloj para controlar FPS

# Posición del jugador
player_pos = pygame.Vector2(posicionInicialAncho, posicionInicialAltura)
ground_level = posicionInicialAltura  # Nivel del suelo

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        # pygame.QUIT es cuando el jugador cierra la pestaña
        if event.type == pygame.QUIT:
            running = False
    x_rel = x % fondo.get_rect().width
    screen.blit(fondo_redimensionado, (x_rel - fondo.get_rect().width, 0))  # Color del fondo de pantalla
    if x_rel < width:
        screen.blit(fondo_redimensionado, (x_rel, 0))
    # Dibujar un círculo que representa al jugador
    pygame.draw.circle(screen, cian, player_pos, 30)
    # Obtener en una variable la tecla presionada
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:        # Movimiento horizontal izquierda
        player_pos.x -= vel
        x += 1                  # Cada vez que se mueva el personaje, el fondo se moverá también
    if keys[pygame.K_d]: # Movimiento horizontal derecha
        player_pos.x += vel
        x -= 1                  # Cada vez que se mueva el personaje, el fondo se moverá también

    # Saltar al presionar espacio y si no está ya saltando
    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            jump_vel = salto  # Velocidad inicial del salto
    else:
        # Simular el salto con movimiento parabólico
        player_pos.y -= jump_vel
        jump_vel -= 1  # Reducir la velocidad de salto por la "gravedad"
        # En caso de que la posicion sea igual que el suelo: parar
        if player_pos.y >= ground_level:
            player_pos.y = ground_level  # Alinear con el suelo
            isJump = False  # Terminar el salto



    pygame.display.flip() # Actualizar la pantalla
    dt = clock.tick(60) / 1000 # Limitar los fps a 60

pygame.quit()
