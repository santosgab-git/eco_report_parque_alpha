# ===========================================
# PLOTS
# ===========================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# ===========================================
# RUTAS
# ===========================================

# Detecta la raíz del proyecto automáticamente
try:
    BASE_DIR = Path(__file__).resolve().parents[1]
except NameError:
    BASE_DIR = Path.cwd()

INPUT_PATH = BASE_DIR / "data/processed/fauna_clean.csv"
OUTPUT_DIR = BASE_DIR / "outputs/figures"

# Crear carpeta de salida si no existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ===========================================
# CARGA
# ===========================================

df = pd.read_csv(INPUT_PATH)

# ===========================================
# GRÁFICO: RIQUEZA TAXONÓMICA
# ===========================================

def plot_riqueza_taxonomica(df, ax):

    resumen = (
        df
        .groupby("Clase")
        .agg({
            "Orden": "nunique",
            "Familia": "nunique",
            "Especie": "nunique"
        })
    )

    if resumen.empty:
        return

    clases = resumen.index
    x = np.arange(len(clases))
    width = 0.25

    # Barras agrupadas
    bars1 = ax.bar(x - width, resumen["Orden"], width,
                   label="Orden", color="#2E7D32")

    bars2 = ax.bar(x, resumen["Familia"], width,
                   label="Familia", color="#1565C0")

    bars3 = ax.bar(x + width, resumen["Especie"], width,
                   label="Especie", color="#F9A825")

    ax.set_xticks(x)
    ax.set_xticklabels(clases)

    ax.set_xlabel("Clase", fontweight="bold", fontsize=12)
    ax.set_ylabel("Riqueza", fontweight="bold", fontsize=12)

    # Leyenda
    legend = ax.legend(title="Categoría",fontsize=11)
    legend.get_title().set_fontweight("bold")

    # Etiquetas de valores
    for bars in [bars1, bars2, bars3]:
        ax.bar_label(
            bars,
            padding=3,
            fontsize=11
        )
        
    # Ajuste dinámico del eje Y
    ymax = resumen.values.max()
    ax.set_ylim(0, ymax * 1.2)

# ===========================================
# GRÁFICO: CLASE vs MANEJO
# ===========================================

def plot_clase_manejo(df, ax):

    resumen = (
        df
        .groupby(["Clase", "Manejo"])["Abundancia"]
        .sum()
        .unstack(fill_value=0)
    )

    # asegurar orden de columnas
    orden = ["Ahuyentamiento", "Rescate"]
    resumen = resumen.reindex(columns=orden)

    # colores personalizados
    colores = {
        "Ahuyentamiento": "#2E7D32",  # verde
        "Rescate": "#1565C0"          # azul
    }

    resumen.plot(
    kind="bar",
    ax=ax,
    color=[colores[col] for col in resumen.columns]
    )

    # etiquetas
    ax.set_xlabel("Clase", fontweight="bold", fontsize=12)
    ax.set_ylabel("Abundancia", fontweight="bold", fontsize=12)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    
    # leyenda
    legend = ax.legend(title="Manejo", fontsize=11)
    legend.get_title().set_fontweight("bold")
    
    
    # etiquetas de datos
    for container in ax.containers:
        ax.bar_label(container, fmt="%d", fontsize=11)
        
# ===========================================
# GRÁFICO: ACTIVIDAD vs MANEJO 
# ===========================================

def plot_actividad_manejo(df, ax):

    # base absoluta
    resumen_abs = (
        df
        .groupby(["Manejo", "Actividad"])["Abundancia"]
        .sum()
        .unstack(fill_value=0)
    )
    
    # abundancia relativa (%)
    resumen_pct = (
    resumen_abs
    .div(resumen_abs.sum(axis=1).replace(0, 1), axis=0)
    * 100
    )
    
    # colores personalizados
    palette = [
    "#66BB6A",  # verde medio claro
    "#90CAF9",  # azul claro
    "#FFB74D",  # naranja suave
    "#FFE082",  # amarillo suave
    "#81C784",  # verde suave
    "#E57373"   # rojo suave
    ]

    # Ordenar actividades por importancia total
    actividades = list(resumen_pct.columns)
    actividades_ordenadas = (
    resumen_abs.sum()
    .sort_values(ascending=False)
    .index.tolist()
    )
    
    colores_actividades = {
        act: palette[i % len(palette)]
        for i, act in enumerate(actividades_ordenadas)
    }

    colores = [colores_actividades[a] for a in actividades]

    resumen_pct.plot(
    kind="barh",
    stacked=True,
    ax=ax,
    color=colores
    )
    
    ax.invert_yaxis()

    # etiquetas
    ax.set_xlabel("Abundancia relativa (%)", fontweight="bold", fontsize=12)
    ax.set_ylabel("")
    
    for label in ax.get_yticklabels():
        label.set_fontweight("bold")
        label.set_fontsize(12)

    # leyenda
    legend = ax.legend(title="Actividad", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=11)
    legend.get_title().set_fontweight("bold")

    ax.set_title("")

    # etiquetas de datos
    for i, container in enumerate(ax.containers):
    
        valores_abs = resumen_abs.iloc[:, i]
    
        labels = [
            f"{int(v)}" if v > 0 else ""
            for v in valores_abs
        ]
    
        ax.bar_label(
          container,
          labels=labels,
          label_type="center",
          fontsize=11,
          color="black"
         )
         
# ===========================================
# FIGURA GENERAL COMPUESTA
# ===========================================

def plot_figura_general(df):

    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(
    2, 2,
    height_ratios=[1, 1.2],
    width_ratios=[1, 1]
    )
    
    axA = fig.add_subplot(gs[0, 0])
    axB = fig.add_subplot(gs[0, 1])
    axC = fig.add_subplot(gs[1, :])

    # Dibujar directamente
    plot_riqueza_taxonomica(df, axA)
    plot_clase_manejo(df, axB)
    plot_actividad_manejo(df, axC)

    # Etiquetas A, B, C
    fig.text(0.05, 0.97, "A", fontsize=18, fontweight='bold')
    fig.text(0.45, 0.97, "B", fontsize=18, fontweight='bold')
    fig.text(0.05, 0.52, "C", fontsize=18, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "figura_general.png", dpi=300)
    plt.close()
    
# ===========================================
# GRÁFICOS TOP N (ESPECIE / ÁREA)
# ===========================================

def plot_top_ax(df, variable, ax):

    resumen = (
        df
        .groupby(variable)["Abundancia"]
        .sum()
        .sort_values(ascending=False)
    )

    if resumen.empty:
        ax.text(0.5, 0.5, "Sin datos", ha="center", va="center")
        ax.axis('off')
        return

    resumen.plot(
        kind="barh",
        color="#2E7D32",
        ax=ax
    )

    ax.invert_yaxis()

    # estilos
    ax.set_xlabel("Abundancia", fontweight="bold", fontsize=12)
    label_y = "Área" if variable == "Area" else variable
    ax.set_ylabel(label_y, fontweight="bold", fontsize=12)
    # tamaño de labels (nombres de especies / áreas)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=10)

    # cursiva para especies
    if variable == "Especie":
        for label in ax.get_yticklabels():
            label.set_fontstyle("italic")

    # etiquetas
    for container in ax.containers:
        ax.bar_label(container, fmt="%d", fontsize=11, padding=3)

    ax.set_title("")
    
    # ampliar eje X
    max_val = resumen.max()
    ax.set_xlim(0, max_val * 1.15)
 
# ===========================================
# FIGURA TOP N COMPUESTA (ESPECIE / ÁREA)
# ===========================================   
def plot_top_general(df, filename=None):

    # =========================
    # ALTURA DINÁMICA
    # =========================
    n_especies = df["Especie"].nunique()
    altura = max(6, n_especies * 0.4)

    fig, axes = plt.subplots(1, 2, figsize=(14, altura))

    axA, axB = axes

    plot_top_ax(df, "Especie", axA)
    plot_top_ax(df, "Area", axB)

    fig.text(0.01, 0.95, "A", fontsize=18, fontweight="bold")
    fig.text(0.57, 0.95, "B", fontsize=18, fontweight="bold")

    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()
        
# ===========================================
# EJECUCIÓN
# ===========================================

if __name__ == "__main__":

    plot_figura_general(df)

    print("Gráfico generado")
    
