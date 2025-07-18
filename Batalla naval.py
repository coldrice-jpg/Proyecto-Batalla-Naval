import pygame
import random
from servidor import Server

# Inicialización del juego
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# Variable del servidor
servidor_host = None
is_server = False
nombre_oponente = ""
oponente_listo = False
juego_lan_iniciado = False
yo_estoy_listo = False 

# Variables a ingresar
nombre_usuario1 = "Host" 
nombre_usuario2 = "Cliente" 
ip_ingresar1 = "127.0.0.1" 
puerto_ingresar1 = "5555" 
ingresar_texto = None
nombre_usuario2 = ""
ip_ingresar2 = ""
puerto_ingresar2 = ""


# Tamaño de la pantalla
tamaño_pantallax = 800
tamaño_pantallay = 600

# Configuración del chat
mensajes_chat = []
MAX_MENSAJES_CHAT = 8
input_chat = ""
input_activo = False


# Cargador de la pantalla
screen = pygame.display.set_mode((tamaño_pantallax, tamaño_pantallay))
pygame.display.set_caption("Batalla Naval")

# Fuentes
fuente1 = pygame.font.SysFont("Calibrí", 30)
fuente2 = pygame.font.SysFont("Calibrí", 25)

# Parametros para los créditos
velocidad_desplazamiento = 1
posicion_y = tamaño_pantallay

# Sonidos
sonido_agua = "assets/sounds/effect_sounds/tiro_agua.mp3"
sonido_impacto = "assets/sounds/effect_sounds/tiro_impacto.mp3"
sonido_agua_obj = pygame.mixer.Sound(sonido_agua)
sonido_impacto_obj = pygame.mixer.Sound(sonido_impacto)

# Cargar sprites para efectos de disparo y fondos
img_tiro_acertado = pygame.image.load("assets/textures/effects/acertado.png").convert_alpha()
img_tiro_fallido = pygame.image.load("assets/textures/effects/fallido.png").convert_alpha()
img_enemigo_acertado = pygame.image.load("assets/textures/effects/fuego.png").convert_alpha()
img_enemigo_fallido = pygame.image.load("assets/textures/effects/disparofallido.png").convert_alpha()

img_tiro_acertado = pygame.transform.scale(img_tiro_acertado, (28, 28))
img_tiro_fallido = pygame.transform.scale(img_tiro_fallido, (28, 28))
img_enemigo_acertado = pygame.transform.scale(img_enemigo_acertado, (28, 28))
img_enemigo_fallido = pygame.transform.scale(img_enemigo_fallido, (28, 28))

imagenmenu = pygame.image.load('assets/textures/backgrounds/imagenmenu.png')
imagenmenu = pygame.transform.scale(imagenmenu, (tamaño_pantallax, tamaño_pantallay))

tira_transparente = pygame.Surface((250, tamaño_pantallay), pygame.SRCALPHA)
tira_transparente.fill((68, 103, 132))
tira_transparente = tira_transparente.convert_alpha()
tira_transparente.set_alpha(180)

# Creditos
creditos_texto = [
    "Batalla naval",
    "",
    "",
    "Desarrollado por: ", 
    "Alexis Fernando Coronado López",
    "",
    "Diseñador: ", 
    "Alexis Fernando Coronado López",
    "",
    "Director de imagen: ", 
    "Alexis Fernando Coronado López",
    "",
    "Assets: ",
    "Backgrounds: Alexis Fernando Coronado López",
    "Barcos: Alexis Fernando Coronado López",
    "",
    "Música menú: Yankee Doodle",
    "Música créditos: Johnny B. Good - Chuck Berry",
    "Música batalla: The Medallions Calls - Klaus Badelt",
    "",
    "",
    "",
    "Pongame 10 profe... no sea malo"
]



# Colores
color_fondo = (0, 0, 0)
verde_oscuro = (0, 145, 80)
verde_claro = (1, 171, 95)
blanco = (255, 255, 255)
azul_claro = (8, 139, 208)
azul_oscuro = (7, 116, 174)
gris = (69, 86, 95)
negro = (0, 0, 0)

# Estado principal
estado_menu = "menu principal"


# Matrices de juego 
tablero_jugador = [[0 for _ in range(10)] for _ in range(10)]
tablero_enemigo = [[0 for _ in range(10)] for _ in range(10)]
disparos_jugador = [[0 for _ in range(10)] for _ in range(10)]
disparos_enemigo = [[0 for _ in range(10)] for _ in range(10)]

# Lista de barcos enemigos
barcos_enemigos = []

# Control de juego
turno_jugador = True
mensaje_estado = ""
juego_terminado = False

# Botones como rectángulos
jugar = pygame.Rect(30, 260, 180, 50)
creditos = pygame.Rect(30, 340, 180, 50)
salir = pygame.Rect(30, 420, 180, 50)
jugar_solo = pygame.Rect(30, 180, 180, 50)
jugar_lan = pygame.Rect(30, 300, 180, 50)
volver = pygame.Rect(30, 420, 180, 50)
creditos_volver = pygame.Rect(10, 550, 100, 40)
crear_partida = pygame.Rect(30, 260, 180,50)
unirse_partida = pygame.Rect(30, 340, 180, 50)
ingresar_host_texto = pygame.Rect(30, 250, 130, 20)
ingresar_host_cuadro = pygame.Rect(30, 260, 180, 20)
cuadro_nombre = pygame.Rect(30, 150, 180, 30)
cuadro_ip = pygame.Rect(30, 250, 180, 30)
cuadro_puerto = pygame.Rect(30, 350, 180, 30)
volver_lan = pygame.Rect(30, 500, 180, 50)
crear_host = pygame.Rect(30, 430, 180, 50)
unirse = pygame.Rect(30, 430, 180, 50)
desertar = pygame.Rect(20, 540, 120, 40)
aleatorio = pygame.Rect(20, 480, 120, 40)
empezar = pygame.Rect(160, 540, 120, 40)
volver_a_jugar = pygame.Rect(250, 400, 200, 60)
rect_input_chat = pygame.Rect(500, 545, 200, 30)  
rect_boton_enviar = pygame.Rect(710, 545, 70, 30)

# Función de atributos de los barcos 
def crear_barco(imagen_camino, posicion_inicial, tamaño_px, tamaño_celdas):
    imagen_original = pygame.image.load(imagen_camino).convert_alpha()
    imagen = pygame.transform.scale(imagen_original, tamaño_px)
    rect = imagen.get_rect(topleft=posicion_inicial)
    return {
        "camino_imagen": imagen_camino,
        "imagen_original": imagen_original,
        "imagen": imagen,
        "rect": rect,
        "posicion_inicial": posicion_inicial,
        "tamaño": tamaño_px,
        "tamaño_celdas": tamaño_celdas,     # <--- NUEVO
        "seleccionado": False,
        "colocado": False,
        "vertical": True,
        "pos_prev": posicion_inicial,
    }

# Generar barcos con sprites
barcos_jugador = [
    crear_barco("assets/textures/boats/portaaviones.png", (50, 335), (28, 135), 5),
    crear_barco("assets/textures/boats/barcogrande.png", (90, 335), (28, 110), 4),
    crear_barco("assets/textures/boats/submarino.png", (130, 355), (28, 80), 3),
    crear_barco("assets/textures/boats/barcopequeño.png", (170, 375), (28, 55), 2),
]

# Matriz de los barcos
barcos_jugador_info = []

# Función para acomodar los barcos en la cuadricula
def pegar_a_cuadricula(x, y): 
    tamaño_cuadricula = 28   
    x_ajustado = 40 + ((x - 40) // tamaño_cuadricula) * tamaño_cuadricula
    y_ajustado = 42 + ((y - 42) // tamaño_cuadricula) * tamaño_cuadricula
    return x_ajustado, y_ajustado

# Función para mandar los mensajes al chat
def agregar_mensaje_chat(texto):
    if len(mensajes_chat) >= MAX_MENSAJES_CHAT:
        mensajes_chat.pop(0)
    mensajes_chat.append(texto)

# Función para que los barcos no se salgan del tablero
def limitar_posicion_barco(rect):
    tablero_x = 40
    tablero_y = 42
    tablero_tamaño = 28 * 10 

    if rect.left < tablero_x:
        rect.left = tablero_x
    if rect.right > tablero_x + tablero_tamaño:
        rect.right = tablero_x + tablero_tamaño

    if rect.top < tablero_y:
        rect.top = tablero_y
    if rect.bottom > tablero_y + tablero_tamaño:
        rect.bottom = tablero_y + tablero_tamaño

    return rect

# Función para que los barcos no se pongan uno encima del otro
def barco_colisiona(barco_actual, barcos):
    for otro in barcos:
        if otro is not barco_actual and otro["colocado"]:
            if barco_actual["rect"].colliderect(otro["rect"]):
                return True
    return False

# Función que actualiza los barcos con cada disparo
def actualizar_tablero_con_barcos(barcos, matriz):
    barcos_jugador_info.clear()
    for barco in barcos:
        x = (barco["rect"].x - 40) // 28
        y = (barco["rect"].y - 42) // 28
        largo = barco["tamaño_celdas"]
        coordenadas = []

        for i in range(largo):
            fila = y + i if barco["vertical"] else y
            col = x if barco["vertical"] else x + i
            if 0 <= fila < 10 and 0 <= col < 10:
                matriz[fila][col] = 1
                coordenadas.append((fila, col))

        if coordenadas:
            barcos_jugador_info.append({
                "coordenadas": coordenadas,
                "impactos": 0,
                "tamaño": largo
            })

# Función que detecta los disparos del jugador
def disparar_jugador(fila, columna):
    global turno_jugador

    if disparos_jugador[fila][columna] != 0:
        return

    disparos_jugador[fila][columna] = 1
    
    if tablero_enemigo[fila][columna] == 1:
        tablero_enemigo[fila][columna] = 2
        agregar_mensaje_chat("[Servidor]: ¡Impacto!")
        sonido_impacto_obj.play()
    else:
        agregar_mensaje_chat("[Servidor]: Tiro fallido.")
        sonido_agua_obj.play()
    
    turno_jugador = False
    pygame.time.set_timer(pygame.USEREVENT, 800)

# Función para dibujar los sprites de los disparos
def dibujar_disparos_con_sprites(matriz_disparos, tablero, origen, es_enemigo=False):
    for fila in range(10):
        for col in range(10):
            if matriz_disparos[fila][col]:
                pos = (origen[0] + col * 28, origen[1] + fila * 28)
                impacto = tablero[fila][col] == 2
                if not es_enemigo:
                    if impacto:
                        screen.blit(img_tiro_acertado, pos)
                    else:
                        screen.blit(img_tiro_fallido, pos)
                else:
                    if impacto:
                        screen.blit(img_enemigo_acertado, pos)
                    else:
                        screen.blit(img_enemigo_fallido, pos)

# Función del disparo del enemigo
def disparo_enemigo():
    global turno_jugador, mensaje_estado, juego_terminado

    if juego_terminado:
        return

    while True:
        fila = random.randint(0, 9)
        col = random.randint(0, 9)
        if disparos_enemigo[fila][col] == 0:
            disparos_enemigo[fila][col] = 1
            if tablero_jugador[fila][col] == 1:
                tablero_jugador[fila][col] = 2
                agregar_mensaje_chat("[Servidor]: ¡El enemigo impactó uno de tus barcos!")
                sonido_impacto_obj.play() 

                for barco in barcos_jugador_info:
                    if (fila, col) in barco["coordenadas"]:
                        barco["impactos"] += 1
                        
                turno_jugador = True
                break
            else:
                sonido_agua_obj.play()
                turno_jugador = True
                break

    pygame.time.set_timer(pygame.USEREVENT, 0)

# Función que detecta si el juego ya termino y dice quien ganó
def revisar_ganador():
    global juego_terminado, mensaje_estado

    if juego_terminado:
        return

    if servidor_host:
        jugador_derrotado = all(celda != 1 for fila in tablero_jugador for celda in fila)
        if jugador_derrotado:
            agregar_mensaje_chat("[Servidor]: ¡Has perdido! Todos tus barcos fueron destruidos.")
            servidor_host.enviar({"type": "game_over"}) 
            juego_terminado = True

    else:
        enemigo_derrotado = all(celda != 1 for fila in tablero_enemigo for celda in fila)
        jugador_derrotado = all(celda != 1 for fila in tablero_jugador for celda in fila)

        if enemigo_derrotado:
            agregar_mensaje_chat("[Servidor]: ¡Ganaste! Has destruido todos los barcos enemigos.")
            juego_terminado = True
        elif jugador_derrotado:
            agregar_mensaje_chat("[Servidor]: Perdiste. El enemigo destruyó tus barcos.")
            juego_terminado = True

# Función que coloca barcos aleatoriamente
def colocar_barcos_aleatoriamente(barcos, filas=10, columnas=10, cuadricula_tamaño=28):
    tablero_x = 40
    tablero_y = 42
    tablero_tamaño = cuadricula_tamaño * 10 

    for barco in barcos:
        colocado = False
        intentos = 0
        while not colocado and intentos < 1000:
            intentos += 1
            vertical = random.choice([True, False])
            barco["vertical"] = vertical

            if vertical:
                alto = barco["tamaño_celdas"]
                ancho = 1
            else:
                ancho = barco["tamaño_celdas"]
                alto = 1

            fila = random.randint(0, filas - alto)
            col = random.randint(0, columnas - ancho)

            x = 40 + col * cuadricula_tamaño
            y = 42 + fila * cuadricula_tamaño

            if vertical:
                barco["imagen"] = pygame.transform.scale(barco["imagen_original"], barco["tamaño"])
            else:
                tamaño_horizontal = (barco["tamaño"][1], barco["tamaño"][0])
                imagen_rotada = pygame.transform.rotate(barco["imagen_original"], -90)
                barco["imagen"] = pygame.transform.scale(imagen_rotada, tamaño_horizontal)

            barco["rect"] = barco["imagen"].get_rect(topleft=(x, y))

            if barco["rect"].right > tablero_x + tablero_tamaño:
                barco["rect"].right = tablero_x + tablero_tamaño
            if barco["rect"].bottom > tablero_y + tablero_tamaño:
                barco["rect"].bottom = tablero_y + tablero_tamaño
            if barco["rect"].left < tablero_x:
                barco["rect"].left = tablero_x
            if barco["rect"].top < tablero_y:
                barco["rect"].top = tablero_y

            if not barco_colisiona(barco, barcos):
                barco["pos_prev"] = (barco["rect"].x, barco["rect"].y)
                barco["colocado"] = True
                colocado = True

# Función que coloca los barcos enemigos
def colocar_barcos_enemigos():
    tipos_barcos = [(5, "portaaviones.png"), (4, "barcogrande.png"), (3, "submarino.png"), (2, "barcopequeño.png")]
    barcos = []
    for tamaño, nombre in tipos_barcos:
        colocado = False
        while not colocado:
            vertical = random.choice([True, False])
            x = random.randint(0, 10 - (1 if vertical else tamaño))
            y = random.randint(0, 10 - (tamaño if vertical else 1))
            colision = False
            for i in range(tamaño):
                fila = y + i if vertical else y
                col = x if vertical else x + i
                if tablero_enemigo[fila][col] == 1:
                    colision = True
                    break
            if not colision:
                for i in range(tamaño):
                    fila = y + i if vertical else y
                    col = x if vertical else x + i
                    tablero_enemigo[fila][col] = 1
                barcos.append({"x": x, "y": y, "tam": tamaño, "vertical": vertical, "impactos": 0})
                colocado = True
    return barcos

# Función que reproduce la musica del juego
def reproducir_musica(ruta, loop=True):
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.play(-1 if loop else 0)

# Función que dibuja el menu principal
def menu_principal():
    logo = pygame.image.load("assets/textures/Logo.png")
    logo = pygame.transform.scale(logo, (280, 210))
    if jugar.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, jugar)
    else:
        pygame.draw.rect(screen, verde_claro, jugar)
    
    if creditos.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen,verde_oscuro, creditos)
    else:
        pygame.draw.rect(screen, verde_claro, creditos)

    if salir.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, salir)
    else:
        pygame.draw.rect(screen, verde_claro, salir)

    texto_jugar = fuente1.render("Jugar", True, blanco)
    texto_creditos = fuente1.render("Creditos", True, blanco)
    texto_salir = fuente1.render("Salir", True, blanco)

    screen.blit(texto_jugar, (jugar.x+(jugar.width-texto_jugar.get_width())/2,
                                jugar.y+(jugar.height-texto_jugar.get_height())/2))
    screen.blit(texto_creditos, (creditos.x+(creditos.width-texto_creditos.get_width())/2,
                                creditos.y+(creditos.height-texto_creditos.get_height())/2))
    screen.blit(texto_salir, (salir.x+(salir.width-texto_salir.get_width())/2,
                                salir.y+(salir.height-texto_salir.get_height())/2))
    screen.blit(logo, (15, 80))

# Función que dibuja el menú de créditos
def menu_creditos(posicion_y):
    
    texto_boton_creditos = fuente1.render("Volver", True, blanco)
    posicion_y -= velocidad_desplazamiento
    
    if posicion_y < -len(creditos_texto) * 40:
        posicion_y = tamaño_pantallay

    screen.fill(color_fondo)
        
    if creditos_volver.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, azul_oscuro, creditos_volver)
    else:
        pygame.draw.rect(screen, azul_claro, creditos_volver)
    screen.blit(texto_boton_creditos, (creditos_volver.x+(creditos_volver.width-texto_boton_creditos.get_width())/2,
                        creditos_volver.y+(creditos_volver.height-texto_boton_creditos.get_height())/2))

    for i, linea in enumerate(creditos_texto):
        texto_superficie = fuente1.render(linea, True, blanco)
        texto_rect = texto_superficie.get_rect(center=(tamaño_pantallax // 2, posicion_y + i * 40))
        screen.blit(texto_superficie, texto_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
    
    return posicion_y

# Función que dibuja el menu jugar
def menu_jugar():
    
    fondo_jugar = pygame.image.load('assets/textures/backgrounds/fondojugar.png')
    fondo_jugar = pygame.transform.scale(fondo_jugar, (tamaño_pantallax, tamaño_pantallay))
    screen.blit(fondo_jugar, (0, 0))
    screen.blit(tira_transparente, (0, 0))
    
    if jugar_solo.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, jugar_solo)
    else:
        pygame.draw.rect(screen, verde_claro, jugar_solo)
    
    if jugar_lan.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, jugar_lan)
    else:
        pygame.draw.rect(screen, verde_claro, jugar_lan)

    if volver.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, volver)
    else:
        pygame.draw.rect(screen, verde_claro, volver)

    texto_solo = fuente1.render("Jugar Solo", True, blanco)
    texto_lan = fuente1.render("Jugar Lan", True, blanco)
    texto_volver = fuente1.render("Volver", True, blanco)

    
    screen.blit(texto_solo, (jugar_solo.x+(jugar_solo.width-texto_solo.get_width())/2,
                            jugar_solo.y+(jugar_solo.height-texto_solo.get_height())/2))
    screen.blit(texto_volver, (volver.x+(volver.width-texto_volver.get_width())/2,
                                volver.y+(volver.height-texto_volver.get_height())/2))
    screen.blit(texto_lan, (jugar_lan.x+(jugar_lan.width-texto_lan.get_width())/2,
                            jugar_lan.y+(jugar_lan.height-texto_lan.get_height())/2))

# Función que dibuja el tablero
def dibujar_tablero(surface, start_x, start_y, tamaño, filas, columnas, color_linea, color_fondo):
    for fila in range(filas):
        for columna in range(columnas):
            rect = pygame.Rect(start_x + columna*tamaño, start_y + fila*tamaño, tamaño, tamaño)
            pygame.draw.rect(surface, color_fondo, rect)
            pygame.draw.rect(surface, color_linea, rect, 1)

# Función que escribe las etiquetas del tablero
def dibujar_etiquetas_tablero(surface, start_x, start_y, tamaño, filas, columnas, fuente, color_texto):
    for col in range(columnas):
        num = fuente.render(str(col + 1), True, color_texto)
        x = start_x + col * tamaño + tamaño // 2 - num.get_width() // 2
        y = start_y - tamaño // 1.2 
        surface.blit(num, (x, y))
    
    for fila in range(filas):
        letra = fuente.render(chr(65 + fila), True, color_texto)  # chr(65) = 'A'
        x = start_x - tamaño // 1.2  # Un poco a la izquierda
        y = start_y + fila * tamaño + tamaño // 2 - letra.get_height() // 2
        surface.blit(letra, (x, y))

# Función que dibuja el menu combate
def menu_combate():
    global turno_jugador, juego_terminado

    fondo = pygame.image.load("assets/textures/backgrounds/fondo_pelea.png")
    fondo = pygame.transform.scale(fondo, (tamaño_pantallax, tamaño_pantallay))
    screen.blit(fondo, (0, 0))
    

    # Dibujar tableros
    dibujar_tablero(screen, 40, 42, 28, 10, 10, azul_oscuro, azul_claro)       # jugador
    dibujar_tablero(screen, 460, 42, 28, 10, 10, gris, blanco)                 # enemigo

    # Etiquetas
    dibujar_etiquetas_tablero(screen, 40, 42, 28, 10, 10, fuente2, blanco)
    dibujar_etiquetas_tablero(screen, 460, 42, 28, 10, 10, fuente2, gris)

    # Dibujar barcos propios
    for barco in barcos_jugador:
        screen.blit(barco["imagen"], barco["rect"].topleft)

    # Disparos
    dibujar_disparos_con_sprites(disparos_jugador, tablero_enemigo, (460, 42), es_enemigo=False)
    dibujar_disparos_con_sprites(disparos_enemigo, tablero_jugador, (40, 42), es_enemigo=True)

    # Botón Desertar
    if desertar.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, desertar)
    else:
        pygame.draw.rect(screen, verde_claro, desertar)

    texto_volver = fuente1.render("Desertar", True, blanco)
    screen.blit(texto_volver, (
        desertar.x + (desertar.width - texto_volver.get_width()) // 2,
        desertar.y + (desertar.height - texto_volver.get_height()) // 2
    ))

    # Mostrar mensaje de estado
    if mensaje_estado:
        texto_estado = fuente1.render(mensaje_estado, True, blanco)
        screen.blit(texto_estado, (
            tamaño_pantallax // 2 - texto_estado.get_width() // 2,
            20
        ))

    # Mostrar mensaje de victoria o derrota
    if juego_terminado:
        mensaje_final = fuente1.render(mensaje_estado, True, blanco)
        screen.blit(mensaje_final, (
            tamaño_pantallax // 2 - mensaje_final.get_width() // 2,
            tamaño_pantallay // 2 - mensaje_final.get_height() // 2
        ))
        
    if juego_terminado:
        mensaje_final = fuente1.render(mensaje_estado, True, blanco)
        screen.blit(mensaje_final, (
            tamaño_pantallax // 2 - mensaje_final.get_width() // 2,
            tamaño_pantallay // 2 - mensaje_final.get_height() // 2 - 30
        ))

        if volver_a_jugar.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, verde_oscuro, volver_a_jugar)
        else:
            pygame.draw.rect(screen, verde_claro, volver_a_jugar)

        texto_reintentar = fuente1.render("Volver a jugar", True, blanco)
        screen.blit(texto_reintentar, (
            volver_a_jugar.x + (volver_a_jugar.width - texto_reintentar.get_width()) // 2,
            volver_a_jugar.y + (volver_a_jugar.height - texto_reintentar.get_height()) // 2
        ))

# Función que dibuja el chat
def dibujar_chat():

    pygame.draw.rect(screen, (20, 20, 20), (500, 350, 280, 190))  # fondo negro
    pygame.draw.rect(screen, blanco, (500, 350, 280, 190), 2)

    # Atributos de los mensajes
    espacio = 20
    x_texto = 510
    y_texto = 355
    max_ancho = 260
    mensajes_renderizados = []

    for mensaje in mensajes_chat[-MAX_MENSAJES_CHAT:]:
        palabras = mensaje.split(" ")
        linea_actual = ""
        for palabra in palabras:
            test_linea = linea_actual + palabra + " "
            render_test = fuente2.render(test_linea, True, blanco)
            if render_test.get_width() < max_ancho:
                linea_actual = test_linea
            else:
                mensajes_renderizados.append(linea_actual.strip())
                linea_actual = palabra + " "
        if linea_actual:
            mensajes_renderizados.append(linea_actual.strip())

    for linea in mensajes_renderizados[-MAX_MENSAJES_CHAT:]:
        texto = fuente2.render(linea, True, blanco)
        screen.blit(texto, (x_texto, y_texto))
        y_texto += espacio

    pygame.draw.rect(screen, negro, rect_input_chat)

    color_borde = azul_claro if input_activo else blanco
    pygame.draw.rect(screen, color_borde, rect_input_chat, 2)

    input_render = fuente2.render(input_chat, True, blanco)
    input_width = rect_input_chat.width - 10

    texto_render = input_chat
    while fuente2.render(texto_render, True, blanco).get_width() > input_width and len(texto_render) > 1:
        texto_render = texto_render[1:]

    texto_input = fuente2.render(texto_render, True, blanco)
    screen.blit(texto_input, (rect_input_chat.x + 5, rect_input_chat.y + 5))

    if rect_boton_enviar.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, rect_boton_enviar)
    else:
        pygame.draw.rect(screen, verde_claro, rect_boton_enviar)
    texto_boton = fuente2.render("Enviar", True, blanco)
    screen.blit(texto_boton, (
        rect_boton_enviar.x + (rect_boton_enviar.width - texto_boton.get_width()) // 2,
        rect_boton_enviar.y + (rect_boton_enviar.height - texto_boton.get_height()) // 2
    ))


# Función que dibuja el menu jugar en solitario
def menu_solo():
    imagenjugar = pygame.image.load("assets/textures/backgrounds/fondo_pelea.png")
    imagenjugar = pygame.transform.scale(imagenjugar, (tamaño_pantallax, tamaño_pantallay))
    screen.blit(imagenjugar, (0, 0))

    dibujar_tablero(screen, 40, 42, 28, 10, 10, azul_oscuro, azul_claro)
    dibujar_etiquetas_tablero(screen, 40, 42, 28, 10, 10, fuente2, blanco)
    
    dibujar_tablero(screen, 460, 42, 28, 10, 10, gris, blanco)
    dibujar_etiquetas_tablero(screen, 460, 42, 28, 10, 10, fuente2, gris)

    for barco in barcos_jugador:
        screen.blit(barco["imagen"], barco["rect"].topleft)

    if aleatorio.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, aleatorio)
    else:
        pygame.draw.rect(screen, verde_claro, aleatorio)
    if desertar.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, desertar)
    else:
        pygame.draw.rect(screen, verde_claro, desertar)
    if empezar.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, empezar)
    else:
        pygame.draw.rect(screen, verde_claro, empezar)

    texto_empezar = fuente1.render("Empezar", True, blanco)
    texto_aleatorio = fuente1.render("Aleatorio", True, blanco)
    texto_volver = fuente1.render("Desertar", True, blanco)

    screen.blit(texto_empezar, (empezar.x+(empezar.width-texto_empezar.get_width())/2,
                                empezar.y+(empezar.height-texto_empezar.get_height())/2))
    screen.blit(texto_aleatorio, (aleatorio.x+(aleatorio.width-texto_aleatorio.get_width())/2,
                                    aleatorio.y+(aleatorio.height-texto_aleatorio.get_height())/2))
    screen.blit(texto_volver, (desertar.x+(desertar.width-texto_volver.get_width())/2,
                                desertar.y+(desertar.height-texto_volver.get_height())/2))


# Función que dibuja el menu jugar en lan
def menu_lan():
    fondo_jugar = pygame.image.load('assets/textures/backgrounds/fondojugar.png')
    fondo_jugar = pygame.transform.scale(fondo_jugar, (tamaño_pantallax, tamaño_pantallay))
    screen.blit(fondo_jugar, (0, 0))
    screen.blit(tira_transparente, (0, 0))
    
    if crear_partida.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, crear_partida)
    else:
        pygame.draw.rect(screen, verde_claro, crear_partida)
    if unirse_partida.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, unirse_partida)
    else:
        pygame.draw.rect(screen, verde_claro, unirse_partida)
    if volver.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, volver)
    else:
        pygame.draw.rect(screen, verde_claro, volver)
    
    texto_crear_partida = fuente1.render("Crear partida", True, blanco)
    texto_unirse_partida = fuente1.render("Unirse a partida", True, blanco)
    texto_volver = fuente1.render("Volver", True, blanco)
    
    screen.blit(texto_crear_partida, (crear_partida.x+(crear_partida.width-texto_crear_partida.get_width())/2,
                                    crear_partida.y+(crear_partida.height-texto_crear_partida.get_height())/2))
    screen.blit(texto_unirse_partida, (unirse_partida.x+(unirse_partida.width-texto_unirse_partida.get_width())/2,
                                        unirse_partida.y+(unirse_partida.height-texto_unirse_partida.get_height())/2))
    screen.blit(texto_volver, (volver.x+(volver.width-texto_volver.get_width())/2,
                                volver.y+(volver.height-texto_volver.get_height())/2))
    
# Función que dibuja el menu crear partida
def partida_host():
    fondo_jugar = pygame.image.load('assets/textures/backgrounds/fondojugar.png')
    fondo_jugar = pygame.transform.scale(fondo_jugar, (tamaño_pantallax, tamaño_pantallay))
    screen.blit(fondo_jugar, (0, 0))
    screen.blit(tira_transparente, (0, 0))
    
    if crear_host.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, crear_host)
    else:
        pygame.draw.rect(screen, verde_claro, crear_host)
    if volver_lan.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, volver_lan)
    else:
        pygame.draw.rect(screen, verde_claro, volver_lan)

    pygame.draw.rect(screen, azul_claro if ingresar_texto == 'nombre1' else blanco, cuadro_nombre, 2)
    texto_nombre_label = fuente2.render("Nombre de usuario:", True, blanco)
    texto_nombre1 = fuente1.render(nombre_usuario1, True, blanco)

    pygame.draw.rect(screen, azul_claro if ingresar_texto == 'ip1' else blanco, cuadro_ip, 2)
    texto_ip_label1 = fuente2.render("Dirección IP del host:", True, blanco)
    texto_ip1 = fuente1.render(ip_ingresar1, True, blanco)

    pygame.draw.rect(screen, azul_claro if ingresar_texto == 'puerto1' else blanco, cuadro_puerto, 2)
    texto_puerto_label1 = fuente2.render("Puerto:", True, blanco)
    texto_puerto1 = fuente1.render(puerto_ingresar1, True, blanco)

    texto_crear_host = fuente1.render("Crear Partida", True, blanco)
    texto_volver = fuente1.render("Volver", True, blanco)

    screen.blit(texto_nombre_label, (cuadro_nombre.x, cuadro_nombre.y - 20))
    screen.blit(texto_nombre1, (cuadro_nombre.x + 5, cuadro_nombre.y + 5))
    
    screen.blit(texto_ip_label1, (cuadro_ip.x, cuadro_ip.y - 20))
    screen.blit(texto_ip1, (cuadro_ip.x + 5, cuadro_ip.y + 5))
    
    screen.blit(texto_puerto_label1, (cuadro_puerto.x, cuadro_puerto.y - 20))
    screen.blit(texto_puerto1, (cuadro_puerto.x + 5, cuadro_puerto.y + 5))
    
    screen.blit(texto_crear_host, (crear_host.x+(crear_host.width-texto_crear_host.get_width())/2,
                                    crear_host.y+(crear_host.height-texto_crear_host.get_height())/2))
    screen.blit(texto_volver, (volver_lan.x+(volver_lan.width-texto_volver.get_width())/2,
                                volver_lan.y+(volver_lan.height-texto_volver.get_height())/2))

# Función que inicia el combate en lan
def iniciar_combate_lan():
    global estado_menu, juego_lan_iniciado, turno_jugador, nombre_oponente

    actualizar_tablero_con_barcos(barcos_jugador, tablero_jugador)
    estado_menu = "menu combate"
    juego_lan_iniciado = True
    
    if is_server:
        turno_jugador = True
        agregar_mensaje_chat("[Servidor]: ¡Ambos listos! Que comience la batalla. Es tu turno.")
    else:
        turno_jugador = False
        agregar_mensaje_chat(f"[Servidor]: ¡Ambos listos! Que comience la batalla. Turno de {nombre_oponente}.")

# Función de espera
def menu_espera():
    fondo_jugar = pygame.image.load('assets/textures/backgrounds/fondojugar.png')
    fondo_jugar = pygame.transform.scale(fondo_jugar, (tamaño_pantallax, tamaño_pantallay))
    screen.blit(fondo_jugar, (0, 0))
    
    texto_espera = fuente1.render("Esperando a un oponente...", True, blanco)
    texto_ip = fuente2.render(f"IP: {ip_ingresar1}  Puerto: {puerto_ingresar1}", True, blanco)
    
    screen.blit(texto_espera, (tamaño_pantallax/2 - texto_espera.get_width()/2, 250))
    screen.blit(texto_ip, (tamaño_pantallax/2 - texto_ip.get_width()/2, 300))

# Función que dibuja el menu para unirse a partida
def partida_unir():
    fondo_jugar = pygame.image.load('assets/textures/backgrounds/fondojugar.png')
    fondo_jugar = pygame.transform.scale(fondo_jugar, (tamaño_pantallax, tamaño_pantallay))
    screen.blit(fondo_jugar, (0, 0))
    screen.blit(tira_transparente, (0, 0))
    
    if unirse.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, unirse)
    else:
        pygame.draw.rect(screen, verde_claro, unirse)
    if volver_lan.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, verde_oscuro, volver_lan)
    else:
        pygame.draw.rect(screen, verde_claro, volver_lan)
        
    pygame.draw.rect(screen, azul_claro if ingresar_texto == 'nombre2' else blanco, cuadro_nombre, 2)
    texto_nombre_label2 = fuente2.render("Nombre de usuario:", True, blanco)
    texto_nombre2 = fuente1.render(nombre_usuario2, True, blanco)

    pygame.draw.rect(screen, azul_claro if ingresar_texto == 'ip2' else blanco, cuadro_ip, 2)
    texto_ip_label2 = fuente2.render("Ingresar ip:", True, blanco)
    texto_ip2 = fuente1.render(ip_ingresar2, True, blanco)

    pygame.draw.rect(screen, azul_claro if ingresar_texto == 'puerto2' else blanco, cuadro_puerto, 2)
    texto_puerto_label2 = fuente2.render("Puerto:", True, blanco)
    texto_puerto2 = fuente1.render(puerto_ingresar2, True, blanco)

    texto_unirse= fuente1.render("Unirse", True, blanco)
    texto_volver = fuente1.render("Volver", True, blanco)

    screen.blit(texto_nombre_label2, (cuadro_nombre.x, cuadro_nombre.y - 20))
    screen.blit(texto_nombre2, (cuadro_nombre.x + 5, cuadro_nombre.y + 5))
    
    screen.blit(texto_ip_label2, (cuadro_ip.x, cuadro_ip.y - 20))
    screen.blit(texto_ip2, (cuadro_ip.x + 5, cuadro_ip.y + 5))
    
    screen.blit(texto_puerto_label2, (cuadro_puerto.x, cuadro_puerto.y - 20))
    screen.blit(texto_puerto2, (cuadro_puerto.x + 5, cuadro_puerto.y + 5))
    
    screen.blit(texto_unirse, (unirse.x+(unirse.width-texto_unirse.get_width())/2,
                                unirse.y+(unirse.height-texto_unirse.get_height())/2))
    screen.blit(texto_volver, (volver_lan.x+(volver_lan.width-texto_volver.get_width())/2,
                                volver_lan.y+(volver_lan.height-texto_volver.get_height())/2))

# Bucle principal
running = True
musica_actual = None
barco_seleccionado_obj = None # Para manejar el barco que se está arrastrando

while running:
    screen.fill(color_fondo)
    screen.blit(imagenmenu, (0, 0))
    screen.blit(tira_transparente, (0, 0))
    
    # Procesar los datos del host
    if servidor_host:
        datos_recibidos = servidor_host.recibir()
        if datos_recibidos:
            tipo_mensaje = datos_recibidos.get("type")

            if tipo_mensaje == "info_usuario":
                nombre_oponente = datos_recibidos["nombre"]
                agregar_mensaje_chat(f"¡{nombre_oponente} se ha unido a la partida!")
            
            elif tipo_mensaje == "listo":
                oponente_listo = True
                agregar_mensaje_chat(f"{nombre_oponente} está listo para el combate.")

                if oponente_listo and yo_estoy_listo:
                    iniciar_combate_lan()

            elif tipo_mensaje == "chat":
                agregar_mensaje_chat(f"[{nombre_oponente}]: {datos_recibidos["mensaje"]}")

            elif tipo_mensaje == "disparo":
                fila, col = datos_recibidos["coordenadas"]
                
                disparos_enemigo[fila][col] = 1
                
                impacto = False
                if tablero_jugador[fila][col] == 1:
                    tablero_jugador[fila][col] = 2
                    impacto = True
                    sonido_impacto_obj.play() 
                else:
                    sonido_agua_obj.play() 
                
                servidor_host.enviar({"type": "resultado_disparo", "coordenadas": [fila, col], "impacto": impacto})
                
                turno_jugador = True
                agregar_mensaje_chat(f"¡{nombre_oponente} ha disparado! Es tu turno.")
                revisar_ganador()

            elif tipo_mensaje == "resultado_disparo":
                fila, col = datos_recibidos["coordenadas"]
                impacto = datos_recibidos["impacto"]
                
                disparos_jugador[fila][col] = 1 
                if impacto:
                    tablero_enemigo[fila][col] = 2 
                    agregar_mensaje_chat("¡Impacto! Turno del oponente.")
                    sonido_impacto_obj.play() 
                else:
                    tablero_enemigo[fila][col] = -1 
                    agregar_mensaje_chat("Agua. Turno del oponente.")
                    sonido_agua_obj.play()
                
                revisar_ganador()

            elif tipo_mensaje == "game_over":
                agregar_mensaje_chat("¡Ganaste! Has destruido todos los barcos enemigos.")
                juego_terminado = True
    
    # Bucle de los eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        pos = pygame.mouse.get_pos()

        # Clicks del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Estado del menu principal
            if estado_menu == "menu principal":
                if salir.collidepoint(pos):
                    running = False
                elif creditos.collidepoint(pos):
                    estado_menu = "menu creditos"
                elif jugar.collidepoint(pos):
                    estado_menu = "menu jugar"
            
            # Estado del menu jugar
            elif estado_menu == "menu jugar":
                if jugar_solo.collidepoint(pos):
                    estado_menu = "menu prepararse"
                elif jugar_lan.collidepoint(pos):
                    estado_menu = "menu lan"
                elif volver.collidepoint(pos):
                    estado_menu = "menu principal"

            # Estado del menu creditos
            elif estado_menu == "menu creditos":
                if creditos_volver.collidepoint(pos):
                    estado_menu = "menu principal"
                    posicion_y = tamaño_pantallay
            
            # Estado del menu lan
            elif estado_menu == "menu lan":
                if volver.collidepoint(pos):
                    estado_menu = "menu jugar"
                elif crear_partida.collidepoint(pos):
                    estado_menu = "menu crear partida"
                elif unirse_partida.collidepoint(pos):
                    estado_menu = "menu unirse partida"
            
            # Estado del menu crear partida
            elif estado_menu == "menu crear partida":
                if crear_host.collidepoint(pos):
                    servidor_host = Server()
                    host = ip_ingresar1
                    puerto = int(puerto_ingresar1)
                    if servidor_host.iniciar_server(host, puerto):
                        is_server = True
                        estado_menu = "esperando oponente"
                elif cuadro_nombre.collidepoint(pos):
                    ingresar_texto = "nombre1"
                elif cuadro_ip.collidepoint(pos):
                    ingresar_texto = "ip1"
                elif cuadro_puerto.collidepoint(pos):
                    ingresar_texto = "puerto1"
                elif volver_lan.collidepoint(pos):
                    estado_menu = "menu lan"
                else:
                    ingresar_texto = None

            # Estado del menu unirse a partida
            elif estado_menu == "menu unirse partida":
                if unirse.collidepoint(pos):
                    servidor_host = Server()
                    host = ip_ingresar2
                    puerto = int(puerto_ingresar2)
                    if servidor_host.conectar_server(host, puerto):
                        is_server = False
                        servidor_host.enviar({"type": "info_usuario", "nombre": nombre_usuario2})
                        estado_menu = "menu prepararse"
                if volver_lan.collidepoint(pos):
                    estado_menu = "menu lan"
                elif cuadro_nombre.collidepoint(pos):
                    ingresar_texto = "nombre2"
                elif cuadro_ip.collidepoint(pos):
                    ingresar_texto = "ip2"
                elif cuadro_puerto.collidepoint(pos):
                    ingresar_texto = "puerto2"
                else:
                    ingresar_texto = None
            
            # Estado para prepararse
            elif estado_menu == "menu prepararse":
                
                if rect_input_chat.collidepoint(pos):
                    input_activo = True
                elif rect_boton_enviar.collidepoint(pos):
                    if input_chat.strip():
                        agregar_mensaje_chat("[Tú]: " + input_chat)
                        if servidor_host:
                            servidor_host.enviar({"type": "chat", "mensaje": input_chat})
                        input_chat = ""
                else: 
                    input_activo = False
                
                if desertar.collidepoint(pos):
                    estado_menu = "menu jugar"
                
                elif empezar.collidepoint(pos):
                    todos_colocados = all(b["colocado"] for b in barcos_jugador)
                    if todos_colocados:
                        if servidor_host:
                            yo_estoy_listo = True
                            agregar_mensaje_chat("[Servidor]: ¡Barcos en posición! Esperando al oponente...")

                            servidor_host.enviar({"type": "listo"})
                            
                            if oponente_listo and yo_estoy_listo:
                                iniciar_combate_lan()
                        else:
                            actualizar_tablero_con_barcos(barcos_jugador, tablero_jugador)
                            barcos_enemigos.clear()
                            for fila in range(10):
                                for col in range(10): tablero_enemigo[fila][col] = 0
                            barcos_enemigos.extend(colocar_barcos_enemigos())
                            estado_menu = "menu combate"
                            agregar_mensaje_chat("[Servidor]: ¡Combate iniciado! Tu turno.")
                    else:
                        agregar_mensaje_chat("[Servidor]: Debes colocar todos los barcos para empezar.")

                elif aleatorio.collidepoint(pos): 
                    colocar_barcos_aleatoriamente(barcos_jugador)
                
                # Interactuar con los barcos con los clicks
                else:
                    for barco in barcos_jugador:
                        if barco["rect"].collidepoint(pos):
                            if event.button == 1:
                                barco["seleccionado"] = True
                                barco_seleccionado_obj = barco
                                break
                            elif event.button == 3:
                                estado_anterior = {
                                    "rect": barco["rect"].copy(),
                                    "imagen": barco["imagen"],
                                    "vertical": barco["vertical"]
                                }
                                barco["vertical"] = not barco["vertical"]
                                if barco["vertical"]:
                                    barco["imagen"] = pygame.transform.scale(barco["imagen_original"], barco["tamaño"])
                                else:
                                    tamaño_horizontal = (barco["tamaño"][1], barco["tamaño"][0])
                                    imagen_rotada = pygame.transform.rotate(barco["imagen_original"], -90)
                                    barco["imagen"] = pygame.transform.scale(imagen_rotada, tamaño_horizontal)

                                barco["rect"] = barco["imagen"].get_rect(topleft=estado_anterior["rect"].topleft)
                                
                                posicion_valida = True
                                tablero_rect = pygame.Rect(40, 42, 280, 280)

                                if barco["rect"].right > tablero_rect.right + 1 or barco["rect"].bottom > tablero_rect.bottom + 1:
                                    posicion_valida = False
                                
                                if barco_colisiona(barco, barcos_jugador):
                                    posicion_valida = False

                                if not posicion_valida:
                                    barco["rect"] = estado_anterior["rect"]
                                    barco["imagen"] = estado_anterior["imagen"]
                                    barco["vertical"] = estado_anterior["vertical"]
                                
                                break 

            # Estado del menu combate
            elif estado_menu == "menu combate":
                if juego_terminado:
                    if volver_a_jugar.collidepoint(pos):
                        tablero_jugador = [[0 for _ in range(10)] for _ in range(10)]
                        tablero_enemigo = [[0 for _ in range(10)] for _ in range(10)]
                        disparos_jugador = [[0 for _ in range(10)] for _ in range(10)]
                        disparos_enemigo = [[0 for _ in range(10)] for _ in range(10)]

                        # Reiniciar barcos del jugador a su posición original
                        for barco in barcos_jugador:
                            barco["colocado"] = False
                            barco["seleccionado"] = False
                            barco["vertical"] = True
                            barco["imagen"] = pygame.transform.scale(barco["imagen_original"], barco["tamaño"])
                            barco["rect"] = barco["imagen"].get_rect(topleft=barco["posicion_inicial"])
                        
                        # Reset de estructuras y estado del juego
                        barcos_jugador_info.clear()
                        barcos_enemigos.clear()
                        mensajes_chat.clear()
                        juego_terminado = False
                        mensaje_estado = ""
                        turno_jugador = True
                        
                        # Reinicio de los estados del lan
                        oponente_listo = False
                        yo_estoy_listo = False
                        juego_lan_iniciado = False
                        
                        # Volver a la pantalla de posicionamiento de barcos
                        estado_menu = "menu prepararse"
                
                # Chat durante el combate
                else:
                    if rect_input_chat.collidepoint(pos):
                        input_activo = True
                    elif rect_boton_enviar.collidepoint(pos):
                        if input_chat.strip():
                            agregar_mensaje_chat("[Tú]: " + input_chat)
                            if servidor_host:
                                servidor_host.enviar({"type": "chat", "mensaje": input_chat})
                            input_chat = ""
                    else:
                        input_activo = False

                    # Lógica de disparo unificada
                    if turno_jugador:
                        # Comprobar si el clic fue en el tablero enemigo
                        if 460 <= pos[0] < 460 + 280 and 42 <= pos[1] < 42 + 280:
                            col = (pos[0] - 460) // 28
                            fila = (pos[1] - 42) // 28
                            
                            if disparos_jugador[fila][col] == 0:
                                if servidor_host:
                                    servidor_host.enviar({"type": "disparo", "coordenadas": [fila, col]})
                                    turno_jugador = False
                                    agregar_mensaje_chat("Has disparado. Esperando resultado...")
                                else:
                                    disparar_jugador(fila, col)
                                    revisar_ganador()

        # Interacción del teclado
        if event.type == pygame.KEYDOWN:
            
            # Estado del menu crear partida
            if estado_menu == "menu crear partida" and ingresar_texto:
                if ingresar_texto == "nombre1":
                    if event.key == pygame.K_BACKSPACE: nombre_usuario1 = nombre_usuario1[:-1]
                    else: nombre_usuario1 += event.unicode
                elif ingresar_texto == "ip1":
                    if event.key == pygame.K_BACKSPACE: ip_ingresar1 = ip_ingresar1[:-1]
                    else: ip_ingresar1 += event.unicode
                elif ingresar_texto == "puerto1":
                    if event.key == pygame.K_BACKSPACE: puerto_ingresar1 = puerto_ingresar1[:-1]
                    else: puerto_ingresar1 += event.unicode
            
            # Estado del menu unirse a partida
            elif estado_menu == "menu unirse partida" and ingresar_texto:
                if ingresar_texto == "nombre2":
                    if event.key == pygame.K_BACKSPACE: nombre_usuario2 = nombre_usuario2[:-1]
                    else: nombre_usuario2 += event.unicode
                elif ingresar_texto == "ip2":
                    if event.key == pygame.K_BACKSPACE: ip_ingresar2 = ip_ingresar2[:-1]
                    else: ip_ingresar2 += event.unicode
                elif ingresar_texto == "puerto2":
                    if event.key == pygame.K_BACKSPACE: puerto_ingresar2 = puerto_ingresar2[:-1]
                    else: puerto_ingresar2 += event.unicode
                    
            # Estado del menu para prepararse
            elif estado_menu == "menu prepararse" and input_activo:
                if event.key == pygame.K_RETURN:
                    if input_chat.strip():
                        agregar_mensaje_chat(f"[Tú]: {input_chat}")
                        if servidor_host:
                            servidor_host.enviar({"type": "chat", "mensaje": input_chat})
                        input_chat = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_chat = input_chat[:-1]
                else:
                    if len(input_chat) < 40:
                        input_chat += event.unicode

            # Estado del menu combate
            elif estado_menu == "menu combate" and input_activo:
                if event.key == pygame.K_RETURN:
                    if input_chat.strip():
                        agregar_mensaje_chat(f"[Tú]: {input_chat}")
                        if servidor_host:
                            servidor_host.enviar({"type": "chat", "mensaje": input_chat})
                        input_chat = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_chat = input_chat[:-1]
                else:
                    if len(input_chat) < 40:
                        input_chat += event.unicode
            
        # Interacción de soltar el click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Estado del menu prepararse
            if estado_menu == "menu prepararse" and barco_seleccionado_obj:
                barco_actual = barco_seleccionado_obj

                tablero_rect = pygame.Rect(40, 42, 280, 280)

                if tablero_rect.collidepoint(pos):
                    x_snap, y_snap = pegar_a_cuadricula(pos[0], pos[1])
                    
                    rect_temporal = barco_actual["imagen"].get_rect(topleft=(x_snap, y_snap))

                    posicion_valida = True

                    if rect_temporal.right > tablero_rect.right + 1 or rect_temporal.bottom > tablero_rect.bottom + 1:
                        posicion_valida = False
                        
                    pos_original = barco_actual["rect"].topleft
                    barco_actual["rect"].topleft = rect_temporal.topleft
                    
                    if barco_colisiona(barco_actual, barcos_jugador):
                        posicion_valida = False
                    
                    barco_actual["rect"].topleft = pos_original

                    if posicion_valida:
                        barco_actual["rect"].topleft = rect_temporal.topleft
                        barco_actual["pos_prev"] = rect_temporal.topleft
                        barco_actual["colocado"] = True
                    else:
                        barco_actual["rect"].topleft = barco_actual["pos_prev"]
                else:
                    barco_actual["rect"].topleft = barco_actual["pos_prev"]

                barco_actual["seleccionado"] = False
                barco_seleccionado_obj = None

        # -Interacción de mover el mouse
        if event.type == pygame.MOUSEMOTION:
            if estado_menu == "menu prepararse" and barco_seleccionado_obj:
                barco_seleccionado_obj["rect"].center = pos
        
        # Disparos del enemigo
        if event.type == pygame.USEREVENT:
            if estado_menu == "menu combate" and not turno_jugador and not juego_terminado:
                disparo_enemigo()
                revisar_ganador()


    # Dibujado de los menus
    if estado_menu == "menu principal":
        if musica_actual != "menu":
            reproducir_musica("assets/sounds/music/yankee-doodle.wav")
            musica_actual = "menu"
        menu_principal()
    elif estado_menu == "menu creditos":
        if musica_actual != "creditos":
            reproducir_musica("assets/sounds/music/johnny-be-goode.wav")
            musica_actual = "creditos"
        posicion_y = menu_creditos(posicion_y)
    elif estado_menu == "menu jugar":
        menu_jugar()
    elif estado_menu == "menu prepararse":
        menu_solo()
        dibujar_chat()
    elif estado_menu == "menu combate":
        if musica_actual != "batalla":
            reproducir_musica("assets/sounds/music/musica_batalla.mp3") 
            musica_actual = "batalla"
        menu_combate()
        dibujar_chat() 
    elif estado_menu == "menu lan":
        menu_lan()
    elif estado_menu == "menu crear partida":
        partida_host()
    elif estado_menu == "esperando oponente":
        menu_espera()
        if servidor_host and servidor_host.aceptar_conexion():
            servidor_host.enviar({"type": "info_usuario", "nombre": nombre_usuario1})
            estado_menu = "menu prepararse"
    elif estado_menu == "menu unirse partida":
        partida_unir()

    pygame.display.flip()

pygame.quit()