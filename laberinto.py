# laberinto.py

import pygame
from collections import deque
from config import TAMANO_CELDA, BLANCO, NEGRO, FILAS, COLUMNAS

# ------------------------------------------------------------
# 0 = camino, 1 = pared
# Definimos 3 laberintos distintos (15x15 cada uno)
# ------------------------------------------------------------

LABERINTO_NIVEL_1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,0,0,1,0,0,0,1,1,1,0],
    [0,0,0,1,0,1,0,1,0,1,0,1,0,0,0],
    [0,1,0,1,0,1,0,0,0,1,0,1,0,1,0],
    [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
    [0,1,0,1,1,1,0,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [0,1,1,1,0,1,1,1,0,1,1,1,0,1,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,1,0,1,1,1,0,1,0,1,1,1,0,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,1,0,1,1,1,0,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [0,1,1,1,0,1,1,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

# Un poco más cerrado en el centro
LABERINTO_NIVEL_2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,1,0,1,0,1,0,1,1,1,0],
    [0,0,0,1,0,1,0,1,0,1,0,1,0,0,0],
    [0,1,0,1,0,1,0,0,0,1,0,1,0,1,0],
    [0,1,0,0,0,0,1,1,1,0,0,0,0,1,0],
    [0,1,0,1,1,0,0,1,0,0,1,1,0,1,0],
    [0,0,0,0,1,0,0,1,0,0,1,0,0,0,0],
    [0,1,1,0,1,1,0,1,0,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,1,1,0,1,1,1,0,1,0,1,0,1,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,1,0,1,1,1,0,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

# Más "laberinto" tipo serpiente
LABERINTO_NIVEL_3 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,1,0,1,1,1,1,1,1,1,1,1,0,1,0],
    [0,1,0,1,0,0,0,0,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,1,1,1,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,0,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,1,1,0,1,1,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

LABERINTOS = [LABERINTO_NIVEL_1, LABERINTO_NIVEL_2, LABERINTO_NIVEL_3]

# laberinto actual
LABERINTO = LABERINTOS[0]
NIVEL_ACTUAL = 1


def set_nivel(nivel: int):
    """
    Cambia el laberinto actual al nivel dado (1, 2 o 3).
    """
    global LABERINTO, NIVEL_ACTUAL
    if nivel < 1 or nivel > len(LABERINTOS):
        nivel = 1
    NIVEL_ACTUAL = nivel
    LABERINTO = LABERINTOS[nivel - 1]


# ------------------------------------------------------------
# Funciones usadas por el juego
# ------------------------------------------------------------

def es_celda_valida(x, y):
    if x < 0 or x >= len(LABERINTO):
        return False
    if y < 0 or y >= len(LABERINTO[0]):
        return False
    return LABERINTO[x][y] == 0


def vecinos_validos(pos):
    x, y = pos
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    res = []
    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if es_celda_valida(nx, ny):
            res.append([nx, ny])
    return res


def celda_libre_mas_cercana(objetivo):
    """
    Devuelve la celda libre (0) más cercana a 'objetivo' (BFS).
    """
    filas = len(LABERINTO)
    columnas = len(LABERINTO[0])
    ox, oy = objetivo
    cola = deque()
    visit = set()

    if 0 <= ox < filas and 0 <= oy < columnas:
        cola.append((ox, oy))
        visit.add((ox, oy))

    while cola:
        x, y = cola.popleft()
        if LABERINTO[x][y] == 0:
            return [x, y]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas and (nx, ny) not in visit:
                visit.add((nx, ny))
                cola.append((nx, ny))

    return [0, 0]


def dibujar_laberinto(superficie):
    filas = len(LABERINTO)
    columnas = len(LABERINTO[0])
    for fila in range(filas):
        for col in range(columnas):
            rect = pygame.Rect(
                col * TAMANO_CELDA,
                fila * TAMANO_CELDA,
                TAMANO_CELDA,
                TAMANO_CELDA,
            )
            color = NEGRO if LABERINTO[fila][col] == 1 else BLANCO
            pygame.draw.rect(superficie, color, rect)
            pygame.draw.rect(superficie, NEGRO, rect, 1)
