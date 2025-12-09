
# 🧠 **Ratón vs Zorro – IA con Aprendizaje por Refuerzo**

### *Proyecto académico de Inteligencia Artificial — SARSA / Q-Learning*

---

## 📌 **Descripción del Proyecto**

Este proyecto implementa un videojuego interactivo donde:

* 🐭 **El jugador controla un ratón**
* 🦊 **Un zorro controlado por IA intenta atraparlo**
* 🧠 La IA combina **Aprendizaje por Refuerzo (SARSA o Q-Learning)** con una arquitectura de control inspirada en el **"Director AI" de Alien: Isolation**.

El objetivo es estudiar cómo técnicas modernas de IA pueden generar **comportamientos agresivos, adaptativos e inteligentes** dentro de un entorno dinámico (laberintos).

El sistema aprende continuamente mediante:

* Recompensas
* Castigos
* Vecindarios del estado
* Modos de comportamiento del Director IA

Además, la IA **guarda su aprendizaje** usando pickle, manteniendo su progreso entre partidas.

---

## 🎮 **Características principales**

### ✔ Tres niveles de laberintos fijos pero distintos

El jugador selecciona el nivel antes de empezar.

### ✔ IA con dos capas:

#### **1. Aprendizaje por Refuerzo**

* SARSA (on-policy)
* Q-learning (off-policy)
* Uso de la ecuación de Bellman
* Proceso de Decisión de Markov (MDP)

#### **2. Director IA (Arquitectura inteligente)**

* Modos de comportamiento:

  * CAZANDO
  * ACECHANDO
  * BUSCANDO
  * RASTRO RECIENTE
  * ZONA CALIENTE
  * EXPLORANDO
* Recuerdo de última posición vista
* Heatmap del movimiento del ratón
* Modulación del epsilon dinámico

### ✔ Registro del aprendizaje y comportamiento

El sistema almacena:

* Q-table (`.pkl`)
* Recompensa por paso (`aprendizaje.csv`)
* Tiempos por partida (`registroTiempo.txt`)

### ✔ Gráficas incluidas

* Recompensa media móvil
* Castigo acumulado
* Curva de aprendizaje (evolución del zorro)
* Tiempo promedio en atrapar al ratón
* Comparación entre niveles

---

## 🗂 **Estructura del Proyecto**

```
proyecto-reforzamiento/
│
├── main.py               # Punto de entrada del juego
├── game.py               # Lógica principal del juego (loop, niveles, estados)
├── rl_agent.py           # Agente del zorro (SARSA / Q-Learning)
├── director_ia.py        # Sistema inteligente de comportamiento
├── laberinto.py          # Definición de los tres niveles de laberinto
├── config.py             # Hiperparámetros y rutas del sistema
│
├── analisis/
│   ├── graficas.py       # Generación de métricas y análisis
│   └── resultados/       # (Opcional) imágenes generadas
│
├── data/
│   └── qtable.pkl        # Memoria persistente del zorro (autogenerada)
│
├── logs/
│   ├── aprendizaje.csv   # Recompensa por paso
│   └── registro.txt      # Movimientos y recompensas
│
├── informe/              # Carpeta ignorada por Git (.gitignore)
│
└── README.md             # Este archivo
```

---

## ⚙️ **Tecnologías utilizadas**

* **Python 3.10+**
* **Pygame** — motor del juego
* **Pickle** — persistencia de la Q-table
* **Numpy / Matemáticas básicas** — cálculos de distancia y estados
* **Aprendizaje por Refuerzo** — SARSA o Q-learning seleccionable
* **Arquitectura IA tipo “Director”** inspirada en videojuegos AAA

---

## 🚀 **Instalación y Ejecución**

### 1. Clonar el repositorio:

```bash
git clone https://github.com/tu_usuario/proyecto-reforzamiento.git
cd proyecto-reforzamiento
```

### 2. Crear entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias:

```bash
pip install pygame numpy matplotlib
```

### 4. Ejecutar el juego:

```bash
python main.py
```

---

## 📊 **Resultados y análisis**

El sistema registra todo el proceso de aprendizaje.
Las gráficas muestran:

* Al inicio, recompensas negativas → exploración y errores.
* Luego, curva ascendente → el zorro aprende rutas óptimas.
* Disminución de castigos → mejor toma de decisiones.
* Tiempos de captura más cortos con entrenamiento prolongado.
* Diferencias de desempeño entre los 3 niveles.

Estas métricas confirman:

> **La IA no solo funciona, sino que realmente aprende y mejora con la experiencia.**

---

## 📝 **Objetivo del proyecto**

Demostrar cómo integrar:

1. **Modelos de Aprendizaje por Refuerzo**
2. **Arquitectura inteligente de control (Director IA)**
3. **Entornos interactivos en tiempo real (videojuego)**

para producir agentes capaces de comportamientos **adaptativos, agresivos e inteligentes**, similares a juegos modernos.

---

## 🏁 **Conclusión**

Este proyecto combina técnicas fundamentales y avanzadas de inteligencia artificial para crear un agente que:

* Aprende del entorno
* Evoluciona su estrategia
* Modifica su comportamiento según contexto
* Mantiene memoria de entrenamiento
* Se adapta al jugador en tiempo real

Es un ejemplo sólido y aplicable de IA moderna dentro de un entorno lúdico, demostrando cómo conceptos teóricos pueden implementarse en sistemas funcionales.

---

## 👤 **Autor**

**Ian Ezequiel Salinas Condori**
Estudiante de Informática – UMSA
Proyecto de Inteligencia Artificial / Aprendizaje por Refuerzo
