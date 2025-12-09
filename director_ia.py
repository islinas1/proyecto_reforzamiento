# director_ia.py

from collections import deque
from laberinto import LABERINTO
import math

def dist_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def linea_de_vision(a, b):
    """
    Línea de visión simple: misma fila o columna sin paredes entre medio.
    """
    lab = LABERINTO
    if a[0] == b[0]:
        fila = a[0]
        y1, y2 = sorted([a[1], b[1]])
        for y in range(y1 + 1, y2):
            if lab[fila][y] == 1:
                return False
        return True
    if a[1] == b[1]:
        col = a[1]
        x1, x2 = sorted([a[0], b[0]])
        for x in range(x1 + 1, x2):
            if lab[x][col] == 1:
                return False
        return True
    return False


class DirectorIA:
    """
    Director estilo Alien:
    - Maneja una 'tensión' global.
    - Recuerda la última posición vista del ratón.
    - Mantiene un pequeño historial (heatmap) de zonas donde el ratón pasa más.
    - Devuelve:
        modo: string ("CAZANDO", "ACECHANDO", "ZONA_CALIENTE", "EXPLORANDO", ...)
        objetivo: celda hacia donde le conviene ir al zorro.
    """

    def __init__(self, max_historial=30):
        self.tension = 0.3
        self.ultima_pos_raton_vista = None
        self.tiempo_sin_ver = 0

        self.historial_raton = deque(maxlen=max_historial)
        self.zonas_calientes = {}   # (x,y) -> veces que el ratón pasó por ahí

        self.modo_actual = "EXPLORANDO"
        self.pasos_en_modo = 0

    # ---------------- helpers internos ----------------

    def _registrar_pos_raton(self, pos_raton):
        pos = tuple(pos_raton)
        self.historial_raton.append(pos)
        self.zonas_calientes[pos] = self.zonas_calientes.get(pos, 0) + 1

    def _zona_caliente_principal(self):
        if not self.zonas_calientes:
            return None
        # celda por la que el ratón ha pasado más veces
        return max(self.zonas_calientes.items(), key=lambda kv: kv[1])[0]

    # ---------------- API principal ----------------

    def actualizar_estado(self, pos_zorro, pos_raton):
        """
        Actualiza la 'tensión', el modo y devuelve (modo, objetivo).

        objetivo es una celda:
          - si ve al ratón -> la posición del ratón
          - si perdió de vista -> la última posición vista
          - si nada de eso -> una zona caliente donde suele pasar el ratón
        """
        self._registrar_pos_raton(pos_raton)
        self.pasos_en_modo += 1

        ve_raton = linea_de_vision(pos_zorro, pos_raton)
        dist = dist_manhattan(pos_zorro, pos_raton)

        # actualizar tensión
        if ve_raton:
            self.ultima_pos_raton_vista = pos_raton[:]
            self.tiempo_sin_ver = 0
            self.tension = min(1.0, self.tension + 0.07)
        else:
            self.tiempo_sin_ver += 1
            self.tension = max(0.0, self.tension - 0.015)

        zona_caliente = self._zona_caliente_principal()

        # --- lógica de modos ---

        # 1) Muy cerca del ratón => CAZANDO
        if dist <= 1:
            self.modo_actual = "CAZANDO"
            objetivo = pos_raton[:]
        # 2) Lo ve y no está muy lejos => ACECHANDO
        elif ve_raton and dist <= 6:
            self.modo_actual = "ACECHANDO"
            objetivo = pos_raton[:]
        # 3) Lo perdió hace poco pero recuerda la última posición => RASTRO
        elif self.ultima_pos_raton_vista is not None and self.tiempo_sin_ver < 10:
            self.modo_actual = "RASTRO_RECIENTE"
            objetivo = self.ultima_pos_raton_vista[:]
        # 4) Tensión moderada/alta y tenemos zona caliente => ir hacia la zona
        elif zona_caliente is not None and self.tension >= 0.4:
            self.modo_actual = "ZONA_CALIENTE"
            objetivo = list(zona_caliente)
        # 5) Nada especial -> EXPLORANDO (seguirá usando solo el ratón como referencia)
        else:
            self.modo_actual = "EXPLORANDO"
            objetivo = pos_raton[:]

        # pequeño reset del contador de pasos cuando cambiamos de modo
        if self.pasos_en_modo > 100:
            self.pasos_en_modo = 0

        return self.modo_actual, objetivo
