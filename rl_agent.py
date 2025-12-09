# rl_agent.py

import pickle
import os
import random
from config import (
    ALPHA, GAMMA,
    EPSILON_INICIAL, EPSILON_MIN, EPSILON_DECAY,
    RUTA_Q_TABLE, RUTA_REGISTRO, RUTA_APRENDIZAJE,
    ALGORITMO_RL
)
from laberinto import es_celda_valida


class RLAgentZorro:
    """
    Agente RL del zorro.
    Soporta SARSA y Q-Learning.
    Incluye shaping hacia un objetivo definido por el Director IA.
    """

    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.epsilon = EPSILON_INICIAL
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY

        self.algoritmo = ALGORITMO_RL.lower()

        # acciones: derecha, abajo, izquierda, arriba
        self.acciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self.q_table = {}
        self.cargar_q_table()

        self.pasos_totales = 0
        self._preparar_log_aprendizaje()

    # --------------------------------------------------
    # Q-TABLE: GUARDAR Y CARGAR
    # --------------------------------------------------
    def guardar_q_table(self):
        """ Guarda la Q-table SIEMPRE que sea llamada. """
        carpeta = os.path.dirname(RUTA_Q_TABLE)
        os.makedirs(carpeta, exist_ok=True)
        with open(RUTA_Q_TABLE, "wb") as f:
            pickle.dump(self.q_table, f)
        print(">> Q-table guardada en:", RUTA_Q_TABLE)

    def cargar_q_table(self):
        """ Carga la Q-table si existe. """
        if os.path.exists(RUTA_Q_TABLE) and os.path.getsize(RUTA_Q_TABLE) > 0:
            with open(RUTA_Q_TABLE, "rb") as f:
                self.q_table = pickle.load(f)
            print(">> Q-table cargada con", len(self.q_table), "estados")
        else:
            self.q_table = {}
            print(">> No existe Q-table previa. Se empezará desde cero.")

    # --------------------------------------------------
    # ESTADO DEL MDP
    # --------------------------------------------------
    def obtener_estado(self, pos_zorro, pos_raton):
        dx = pos_raton[0] - pos_zorro[0]
        dy = pos_raton[1] - pos_zorro[1]

        dx = max(-3, min(3, dx))
        dy = max(-3, min(3, dy))

        arriba = 0 if es_celda_valida(pos_zorro[0] - 1, pos_zorro[1]) else 1
        abajo  = 0 if es_celda_valida(pos_zorro[0] + 1, pos_zorro[1]) else 1
        izq    = 0 if es_celda_valida(pos_zorro[0], pos_zorro[1] - 1) else 1
        der    = 0 if es_celda_valida(pos_zorro[0], pos_zorro[1] + 1) else 1

        return (dx, dy, arriba, abajo, izq, der)

    # --------------------------------------------------
    # POLÍTICA ε-GREEDY
    # --------------------------------------------------
    def seleccionar_accion_con(self, epsilon, estado):
        if random.uniform(0, 1) < epsilon:
            return random.choice(self.acciones)

        q_vals = self.q_table.get(estado, [0, 0, 0, 0])
        max_q = max(q_vals)
        mejores = [self.acciones[i] for i, q in enumerate(q_vals) if q == max_q]
        return random.choice(mejores)

    # --------------------------------------------------
    # BACKUPS DE BELLMAN
    # --------------------------------------------------
    def _backup_q_learning(self, estado, accion, recompensa, siguiente_estado, done):
        if estado not in self.q_table:
            self.q_table[estado] = [0, 0, 0, 0]
        if siguiente_estado not in self.q_table:
            self.q_table[siguiente_estado] = [0, 0, 0, 0]

        idx = self.acciones.index(accion)
        max_q_next = 0 if done else max(self.q_table[siguiente_estado])
        viejo = self.q_table[estado][idx]
        objetivo = recompensa + self.gamma * max_q_next
        self.q_table[estado][idx] = viejo + self.alpha * (objetivo - viejo)

    def _backup_sarsa(self, estado, accion, recompensa, siguiente_estado, siguiente_accion, done):
        if estado not in self.q_table:
            self.q_table[estado] = [0, 0, 0, 0]
        if siguiente_estado not in self.q_table:
            self.q_table[siguiente_estado] = [0, 0, 0, 0]

        idx = self.acciones.index(accion)
        idx_next = self.acciones.index(siguiente_accion)
        q_next = 0 if done else self.q_table[siguiente_estado][idx_next]
        viejo = self.q_table[estado][idx]
        objetivo = recompensa + self.gamma * q_next
        self.q_table[estado][idx] = viejo + self.alpha * (objetivo - viejo)

    # --------------------------------------------------
    # ENTRENAMIENTO DEL AGENTE
    # --------------------------------------------------
    def paso_entrenamiento(self, pos_zorro, pos_raton, modo="EXPLORANDO", objetivo=None):

        estado = self.obtener_estado(pos_zorro, pos_raton)

        # epsilon dinámico según estado emocional del director
        eps_step = self.epsilon
        if modo == "ACECHANDO":
            eps_step *= 0.5
        elif modo == "CAZANDO":
            eps_step *= 0.2

        accion = self.seleccionar_accion_con(eps_step, estado)

        # movimiento tentativa
        nx = pos_zorro[0] + accion[0]
        ny = pos_zorro[1] + accion[1]

        # colisión con muro
        if not es_celda_valida(nx, ny):
            nueva_pos = pos_zorro[:]
            recompensa = -3.0
        else:
            nueva_pos = [nx, ny]
            recompensa = -0.05

        # objetivo del Director IA
        objetivo_ref = objetivo if objetivo is not None else pos_raton

        dist_prev = abs(pos_zorro[0] - objetivo_ref[0]) + abs(pos_zorro[1] - objetivo_ref[1])
        dist_new  = abs(nueva_pos[0] - objetivo_ref[0]) + abs(nueva_pos[1] - objetivo_ref[1])

        if dist_new < dist_prev:
            recompensa += 0.4
        elif dist_new > dist_prev:
            recompensa -= 0.2

        # ¿Atrapó al ratón?
        done = False
        if nueva_pos == pos_raton:
            recompensa += 20.0
            done = True

        siguiente_estado = self.obtener_estado(nueva_pos, pos_raton)

        # actualización según algoritmo
        if self.algoritmo == "sarsa":
            siguiente_accion = self.seleccionar_accion_con(eps_step, siguiente_estado)
            self._backup_sarsa(estado, accion, recompensa, siguiente_estado, siguiente_accion, done)
        else:
            self._backup_q_learning(estado, accion, recompensa, siguiente_estado, done)

        # actualizar epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # logging
        self.pasos_totales += 1
        self._log_step(self.pasos_totales, recompensa)
        self._registrar_movimiento_txt(estado, accion, nueva_pos, recompensa)

        return nueva_pos, done

    # --------------------------------------------------
    # LOGGING
    # --------------------------------------------------
    def _preparar_log_aprendizaje(self):
        os.makedirs(os.path.dirname(RUTA_APRENDIZAJE), exist_ok=True)
        if not os.path.exists(RUTA_APRENDIZAJE):
            with open(RUTA_APRENDIZAJE, "w", encoding="utf-8") as f:
                f.write("step,reward\n")

    def _log_step(self, step, reward):
        with open(RUTA_APRENDIZAJE, "a", encoding="utf-8") as f:
            f.write(f"{step},{reward}\n")

    def _registrar_movimiento_txt(self, estado, accion, nueva_pos, recompensa):
        os.makedirs(os.path.dirname(RUTA_REGISTRO), exist_ok=True)
        with open(RUTA_REGISTRO, "a", encoding="utf-8") as log:
            log.write(
                f"Estado: {estado}, Acción: {accion}, Nueva posición: {nueva_pos}, "
                f"Recompensa: {recompensa}\n"
            )
