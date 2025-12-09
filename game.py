# game.py

import pygame
import sys
import time
import os

from config import (
    ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, GRIS_CLARO, GRIS_OSCURO,
    AZUL, VERDE, ROJO, FONDO_MENU, FONDO_PANEL,
    MENU_PRINCIPAL, JUGANDO, VICTORIA_RATON, VICTORIA_ZORRO,
    FPS, INTERVALO_MOVIMIENTO_ZORRO, RUTA_TIEMPOS, TAMANO_CELDA,
    FILAS, COLUMNAS
)
import laberinto as lb
from rl_agent import RLAgentZorro
from director_ia import DirectorIA


def dibujar_texto(pantalla, texto, tamano, color, x, y, centro=False):
    fuente = pygame.font.Font(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    pantalla.blit(superficie, rect)


def registrar_tiempo(segundos, ganador):
    """
    Guarda el resultado de cada partida.
    ganador: "ZORRO" o "RATON"
    """
    os.makedirs(os.path.dirname(RUTA_TIEMPOS), exist_ok=True)
    with open(RUTA_TIEMPOS, "a", encoding="utf-8") as log:
        log.write(f"{ganador},{segundos:.2f}\n")


def mostrar_graficas_aprendizaje():
    try:
        from analisis.graficas import mostrar_graficas
        mostrar_graficas()
    except Exception as e:
        print("Error al mostrar gráficas:", e)


def dibujar_menu_principal(pantalla, imagen_raton=None, imagen_zorro=None):
    pantalla.fill(FONDO_MENU)

    panel_rect = pygame.Rect(40, 40, ANCHO_PANTALLA - 80, ALTO_PANTALLA - 140)
    pygame.draw.rect(pantalla, FONDO_PANEL, panel_rect, border_radius=15)
    pygame.draw.rect(pantalla, GRIS_OSCURO, panel_rect, 2, border_radius=15)

    dibujar_texto(pantalla, "Ratón vs Zorro", 40, AZUL,
                  ANCHO_PANTALLA // 2, 80, centro=True)
    dibujar_texto(pantalla, "Aprendizaje por Refuerzo (SARSA / Q-Learning)", 22, GRIS_OSCURO,
                  ANCHO_PANTALLA // 2, 115, centro=True)

    dibujar_texto(pantalla, "Elige nivel:", 26, GRIS_OSCURO,
                  ANCHO_PANTALLA // 2, 165, centro=True)
    dibujar_texto(pantalla, "1. Nivel 1  |  2. Nivel 2  |  3. Nivel 3", 24, VERDE,
                  ANCHO_PANTALLA // 2, 200, centro=True)

    dibujar_texto(pantalla, "4. Ver gráficas de aprendizaje", 24, GRIS_OSCURO,
                  ANCHO_PANTALLA // 2, 250, centro=True)
    dibujar_texto(pantalla, "5. Salir", 24, ROJO,
                  ANCHO_PANTALLA // 2, 285, centro=True)

    dibujar_texto(pantalla, "Usa las flechas para mover al Ratón", 22, GRIS_OSCURO,
                  ANCHO_PANTALLA // 2, 335, centro=True)

    if imagen_raton is not None:
        pantalla.blit(imagen_raton, (panel_rect.left + 15, panel_rect.bottom - 60))
    if imagen_zorro is not None:
        pantalla.blit(imagen_zorro, (panel_rect.right - TAMANO_CELDA - 15,
                                     panel_rect.bottom - 60))


def inicializar_nivel(nivel_actual):
    """
    Configura LABERINTO y posiciones iniciales según el nivel.
    Devuelve: pos_queso, pos_raton, pos_zorro, agente_zorro, director
    """
    lb.set_nivel(nivel_actual)

    pos_queso = lb.celda_libre_mas_cercana((FILAS - 1, COLUMNAS - 1))
    pos_inicial_raton = lb.celda_libre_mas_cercana((0, 0))
    pos_inicial_zorro = lb.celda_libre_mas_cercana((FILAS - 1, 0))

    pos_raton = pos_inicial_raton[:]
    pos_zorro = pos_inicial_zorro[:]

    agente_zorro = RLAgentZorro(lb.LABERINTO)
    director = DirectorIA()

    return pos_queso, pos_raton, pos_zorro, agente_zorro, director


def run_game():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Ratón (jugador) vs Zorro (IA)")
    clock = pygame.time.Clock()

    imagen_raton = pygame.image.load("assets/imagenes/mouse.png")
    imagen_queso = pygame.image.load("assets/imagenes/cheese.jpg")
    imagen_zorro = pygame.image.load("assets/imagenes/zorro.png")
    imagen_raton = pygame.transform.scale(imagen_raton, (TAMANO_CELDA, TAMANO_CELDA))
    imagen_queso = pygame.transform.scale(imagen_queso, (TAMANO_CELDA, TAMANO_CELDA))
    imagen_zorro = pygame.transform.scale(imagen_zorro, (TAMANO_CELDA, TAMANO_CELDA))

    # Nivel por defecto (si entra directo a juego desde código)
    nivel_actual = 1
    pos_queso, pos_raton, pos_zorro, agente_zorro, director = inicializar_nivel(nivel_actual)

    estado_juego = MENU_PRINCIPAL
    contador_mov_zorro = 0
    inicio_tiempo = None
    tiempo_transcurrido = 0

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # -------- MENÚ PRINCIPAL: elegir nivel --------
            if estado_juego == MENU_PRINCIPAL and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    nivel_actual = 1
                    pos_queso, pos_raton, pos_zorro, agente_zorro, director = inicializar_nivel(nivel_actual)
                    inicio_tiempo = time.time()
                    estado_juego = JUGANDO

                elif event.key == pygame.K_2:
                    nivel_actual = 2
                    pos_queso, pos_raton, pos_zorro, agente_zorro, director = inicializar_nivel(nivel_actual)
                    inicio_tiempo = time.time()
                    estado_juego = JUGANDO

                elif event.key == pygame.K_3:
                    nivel_actual = 3
                    pos_queso, pos_raton, pos_zorro, agente_zorro, director = inicializar_nivel(nivel_actual)
                    inicio_tiempo = time.time()
                    estado_juego = JUGANDO

                elif event.key == pygame.K_4:
                    mostrar_graficas_aprendizaje()

                elif event.key == pygame.K_5:
                    running = False

            # -------- CONTROLES DURANTE EL JUEGO --------
            if estado_juego == JUGANDO and event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_UP:
                    dx, dy = -1, 0
                elif event.key == pygame.K_DOWN:
                    dx, dy = 1, 0
                elif event.key == pygame.K_LEFT:
                    dx, dy = 0, -1
                elif event.key == pygame.K_RIGHT:
                    dx, dy = 0, 1

                nx, ny = pos_raton[0] + dx, pos_raton[1] + dy
                if lb.es_celda_valida(nx, ny):
                    pos_raton = [nx, ny]

            # -------- OPCIONES TRAS GANAR/PERDER --------
            if estado_juego in (VICTORIA_RATON, VICTORIA_ZORRO) and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Reiniciar el mismo nivel
                    pos_queso, pos_raton, pos_zorro, agente_zorro, director = inicializar_nivel(nivel_actual)
                    inicio_tiempo = time.time()
                    estado_juego = JUGANDO
                elif event.key == pygame.K_2:
                    # Volver al menu
                    estado_juego = MENU_PRINCIPAL
                elif event.key == pygame.K_3:
                    running = False

        # ----------------- LOGICA -----------------
        if estado_juego == JUGANDO:
            contador_mov_zorro += 1
            if contador_mov_zorro >= INTERVALO_MOVIMIENTO_ZORRO:
                modo, objetivo = director.actualizar_estado(pos_zorro, pos_raton)
                pos_zorro, atrapado = agente_zorro.paso_entrenamiento(
                    pos_zorro,
                    pos_raton,
                    modo=modo,
                    objetivo=objetivo,
                )
                contador_mov_zorro = 0
                if atrapado:
                    estado_juego = VICTORIA_ZORRO
                    tiempo_transcurrido = time.time() - inicio_tiempo
                    registrar_tiempo(tiempo_transcurrido, "ZORRO")
                    agente_zorro.guardar_q_table()   


            if pos_raton == pos_queso:
                estado_juego = VICTORIA_RATON
                tiempo_transcurrido = time.time() - inicio_tiempo
                registrar_tiempo(tiempo_transcurrido, "RATON")
                agente_zorro.guardar_q_table()  

        # ----------------- DIBUJO -----------------
        if estado_juego == MENU_PRINCIPAL:
            dibujar_menu_principal(pantalla, imagen_raton, imagen_zorro)
            pygame.display.flip()
            continue

        pantalla.fill(GRIS_CLARO)
        pygame.draw.rect(pantalla, BLANCO, (0, 0, ANCHO_PANTALLA, 70))
        pygame.draw.line(pantalla, GRIS_OSCURO, (0, 70), (ANCHO_PANTALLA, 70), 2)

        if inicio_tiempo is not None and estado_juego == JUGANDO:
            t = time.time() - inicio_tiempo
            dibujar_texto(pantalla, f"Tiempo: {t:.2f}s", 24, AZUL, 10, 10)
            dibujar_texto(pantalla, f"Epsilon: {agente_zorro.epsilon:.3f}", 24, AZUL, 10, 38)

        superficie_laberinto = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA - 70))
        superficie_laberinto.fill(GRIS_CLARO)
        lb.dibujar_laberinto(superficie_laberinto)

        superficie_laberinto.blit(
            imagen_queso,
            (pos_queso[1] * TAMANO_CELDA, pos_queso[0] * TAMANO_CELDA),
        )
        superficie_laberinto.blit(
            imagen_raton,
            (pos_raton[1] * TAMANO_CELDA, pos_raton[0] * TAMANO_CELDA),
        )
        superficie_laberinto.blit(
            imagen_zorro,
            (pos_zorro[1] * TAMANO_CELDA, pos_zorro[0] * TAMANO_CELDA),
        )

        pantalla.blit(superficie_laberinto, (0, 70))

        if estado_juego == VICTORIA_RATON:
            dibujar_texto(pantalla, "¡Ganaste, llegaste al queso!", 30, AZUL,
                          ANCHO_PANTALLA // 2, 110, centro=True)
            dibujar_texto(pantalla, f"Tiempo: {tiempo_transcurrido:.2f}s", 26, VERDE,
                          ANCHO_PANTALLA // 2, 145, centro=True)
            dibujar_texto(pantalla, "1. Reiniciar nivel   2. Menú   3. Salir", 24, ROJO,
                          ANCHO_PANTALLA // 2, 180, centro=True)

        if estado_juego == VICTORIA_ZORRO:
            dibujar_texto(pantalla, "El zorro te atrapó", 30, ROJO,
                          ANCHO_PANTALLA // 2, 110, centro=True)
            dibujar_texto(pantalla, f"Tiempo: {tiempo_transcurrido:.2f}s", 26, VERDE,
                          ANCHO_PANTALLA // 2, 145, centro=True)
            dibujar_texto(pantalla, "1. Reiniciar nivel   2. Menú   3. Salir", 24, ROJO,
                          ANCHO_PANTALLA // 2, 180, centro=True)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
