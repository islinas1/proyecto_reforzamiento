# config.py

# --- Tamaños ---
TAMANO_CELDA = 32
FILAS = 15
COLUMNAS = 15

ANCHO_PANTALLA = TAMANO_CELDA * COLUMNAS
ALTO_PANTALLA = TAMANO_CELDA * FILAS + 70  # + HUD arriba

# --- Colores ---
BLANCO      = (255, 255, 255)
NEGRO       = (0, 0, 0)
AZUL        = (40, 120, 255)
VERDE       = (0, 220, 80)
ROJO        = (230, 40, 40)
GRIS_CLARO  = (230, 230, 230)
GRIS_OSCURO = (60, 60, 60)
FONDO_MENU  = (15, 20, 40)
FONDO_PANEL = (245, 245, 255)

# --- Estados del juego ---
MENU_PRINCIPAL = 0
JUGANDO        = 1
VICTORIA_RATON = 2
VICTORIA_ZORRO = 3

# --- Parámetros de RL ---
ALPHA           = 0.25
GAMMA           = 0.95
EPSILON_INICIAL = 0.8
EPSILON_MIN     = 0.05
EPSILON_DECAY   = 0.995

# Elegir algoritmo de RL: "sarsa" o "q_learning"
ALGORITMO_RL = "sarsa"

# --- Archivos ---
RUTA_Q_TABLE     = "data/q_table.pkl"
RUTA_REGISTRO    = "logs/registro.txt"
RUTA_TIEMPOS     = "logs/registroTiempo.txt"
RUTA_APRENDIZAJE = "logs/aprendizaje_rl.csv"

# --- FPS ---
FPS = 60

# Cada cuántos frames se mueve el zorro (menos = más agresivo)
INTERVALO_MOVIMIENTO_ZORRO = 7
