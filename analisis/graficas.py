# analisis/graficas.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from config import RUTA_APRENDIZAJE, RUTA_TIEMPOS


def grafica_recompensa_media():
    if not os.path.exists(RUTA_APRENDIZAJE):
        print("No existe el archivo de aprendizaje:", RUTA_APRENDIZAJE)
        return

    df = pd.read_csv(RUTA_APRENDIZAJE)
    if "step" not in df.columns or "reward" not in df.columns:
        print("Formato inesperado en", RUTA_APRENDIZAJE)
        return

    # media móvil en ventana de 200 pasos (puedes cambiar 200)
    df["reward_ma"] = df["reward"].rolling(window=200, min_periods=1).mean()

    plt.figure(figsize=(8, 5))
    plt.plot(df["step"], df["reward_ma"])
    plt.xlabel("Paso")
    plt.ylabel("Recompensa media (ventana=200)")
    plt.title("Curva de aprendizaje del zorro (recompensa media)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def grafica_recompensa_acumulada():
    if not os.path.exists(RUTA_APRENDIZAJE):
        print("No existe el archivo de aprendizaje:", RUTA_APRENDIZAJE)
        return

    df = pd.read_csv(RUTA_APRENDIZAJE)
    if "step" not in df.columns or "reward" not in df.columns:
        print("Formato inesperado en", RUTA_APRENDIZAJE)
        return

    df["reward_pos"] = df["reward"].clip(lower=0)
    df["reward_neg"] = df["reward"].clip(upper=0)

    df["cum_pos"] = df["reward_pos"].cumsum()
    df["cum_neg"] = df["reward_neg"].cumsum()

    plt.figure(figsize=(8, 5))
    plt.plot(df["step"], df["cum_pos"], label="Recompensa acumulada (+)")
    plt.plot(df["step"], df["cum_neg"], label="Castigo acumulado (-)")
    plt.xlabel("Paso")
    plt.ylabel("Valor acumulado")
    plt.title("Aprendizaje del zorro (recompensa vs castigo)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def grafica_winrate_y_tiempos():
    if not os.path.exists(RUTA_TIEMPOS):
        print("No existe el archivo de tiempos:", RUTA_TIEMPOS)
        return

    # leemos como CSV con dos columnas: ganador, tiempo
    df = pd.read_csv(
        RUTA_TIEMPOS,
        header=None,
        names=["ganador", "tiempo"],
    )

    # Win-rate del zorro en ventana de 20 partidas
    df["win_zorro"] = (df["ganador"] == "ZORRO").astype(int)
    df["winrate_zorro_ma"] = df["win_zorro"].rolling(window=20, min_periods=1).mean()

    # tiempos medios
    prom_zorro = df.loc[df["ganador"] == "ZORRO", "tiempo"].mean()
    prom_raton = df.loc[df["ganador"] == "RATON", "tiempo"].mean()

    # Figura 1: win-rate
    plt.figure(figsize=(8, 4))
    plt.plot(df.index + 1, df["winrate_zorro_ma"])
    plt.xlabel("Partida")
    plt.ylabel("Win-rate (ventana=20)")
    plt.ylim(0, 1)
    plt.title("Tasa de victorias del zorro")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Imprimir resumen de tiempos
    print("Tiempo medio cuando gana el ZORRO:", prom_zorro)
    print("Tiempo medio cuando gana el RATON:", prom_raton)


def mostrar_graficas():
    print("Mostrando: recompensa media móvil...")
    grafica_recompensa_media()
    print("Mostrando: recompensa/castigo acumulados...")
    grafica_recompensa_acumulada()
    print("Mostrando: win-rate y tiempos...")
    grafica_winrate_y_tiempos()


if __name__ == "__main__":
    mostrar_graficas()
