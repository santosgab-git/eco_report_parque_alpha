# Automatización de reportes técnicos ambientales

Proyecto de análisis de datos ecológicos orientado a la automatización de reportes técnicos ambientales, integrando R, Python y generación reproducible de documentos.

## 🎯 Objetivo

Desarrollar un flujo de trabajo reproducible para:

- Procesar datos de monitoreo de fauna
- Generar indicadores ecológicos
- Construir tablas técnicas listas para informes
- Automatizar la redacción de resultados
- Exportar reportes en formato Word/PDF

## 🐾 Dataset

El dataset corresponde a registros de manejo de fauna en campo, incluyendo:

- Eventos de rescate y ahuyentamiento
- Variables taxonómicas (Clase, Orden, Familia, Especie)
- Variables operativas (Área, Abundancia, Manejo)
- Variables de conservación (UICN, CITES, Distribución)

Los datos provienen de monitoreos ambientales asociados a actividades de obra y manejo de biodiversidad.


## ⚙️ Tecnologías utilizadas

- **R**
  - dplyr, tidyr (procesamiento)

  - knitr, kableExtra (tablas)
  - Quarto (reportes)

- **Python**
  - pandas (transformación de datos)
  - matplotlib (visualización)

- **Integración**
  - reticulate (R + Python)


## 📊 Funcionalidades principales

### 🔹 Generación automática de texto técnico

- Redacción dinámica por grupo faunístico:
  - Abundancia
  - Riqueza taxonómica
  - Especies dominantes
  - Distribución espacial
- Lógica adaptable a:
  - Rescate
  - Ahuyentamiento
  - Casos sin registros


### 🔹 Tablas ecológicas jerárquicas

- Estructura taxonómica:
  - Orden → Familia → Especie
- Integración de:
  - CITES
  - UICN
  - Distribución
- Totales automáticos
- Formato listo para LaTeX / Word


### 🔹 Visualización automática

- Gráficos de:
  - Abundancia por especie
  - Abundancia por área
- Escalado dinámico según número de especies


### 🔹 Sección de conservación automatizada

- Clasificación UICN
- Identificación de especies en riesgo
- Inclusión en CITES
- Detección de endemismo


## 🔁 Flujo de trabajo

1. Ingesta de datos de campo
2. Procesamiento y limpieza (R / Python)
3. Generación de tablas y gráficos
4. Construcción automática de texto
5. Exportación de reporte final


## 📁 Estructura del proyecto
.
├── assets/                 # Recursos auxiliares
├── config/                 # Configuración del proyecto
│
├── data/
│   ├── raw/                # Datos originales
│   ├── processed/          # Datos limpios
│   └── lookup/             # Tablas de referencia
│
├── outputs/
│   ├── figures/            # Figuras generadas
│   └── tables/             # Tablas exportadas
│
├── scripts/
│   ├── 01_cleaning.R       # Limpieza de datos
│   ├── 02_tables.R         # Generación de tablas
│   ├── 03_plots.R          # Visualizaciones
│   └── Run_all.R           # Ejecución completa
│
├── report/
│   └── report.qmd          # Reporte en Quarto
│
└── README.md

🔁 Reproducibilidad

Este proyecto fue diseñado como un flujo de trabajo completamente reproducible.

Para ejecutar el análisis completo:

source("scripts/Run_all.R")

Este script ejecuta de forma secuencial:

01_cleaning.py
02_tables.py
03_plots.py

Una vez finalizado, se puede generar el reporte técnico en PDF con:

quarto render report/report.qmd