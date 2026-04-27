# 🌿 Análisis Ecológico y Automatización de Reportes de Fauna

## 🎯 Objetivo

Desarrollar un flujo de trabajo reproducible para el análisis de datos de fauna en proyectos ambientales, permitiendo:

- Evaluar indicadores de manejo (rescate y ahuyentamiento)  
- Analizar abundancia, riqueza y distribución de especies  
- Generar tablas técnicas listas para informes  
- Automatizar la redacción de resultados ecológicos  
- Construir reportes técnicos reproducibles en Word/PDF  

## 🐾 Dataset

El dataset corresponde a registros de manejo de fauna en campo, incluyendo:

- Eventos de **rescate y ahuyentamiento**  
- Variables taxonómicas:
  - Clase, Orden, Familia, Especie  
- Variables operativas:
  - Área, Abundancia, Manejo  
- Variables de conservación:
  - UICN, CITES, Distribución  

Los datos provienen de monitoreos ambientales asociados a actividades de obra y manejo de biodiversidad.

## 🧰 Herramientas utilizadas

- **R** → análisis y automatización  
- **tidyverse** → manipulación de datos  
- **knitr / kableExtra** → tablas técnicas  
- **Quarto** → reporte reproducible  
- **Python (pandas, matplotlib)** → transformación y visualización  
- **reticulate** → integración R + Python  

## 🔬 Metodología

El análisis se desarrolló como un flujo de trabajo reproducible:

### 1. Limpieza de datos

- Validación de estructura  
- Estandarización de variables  
- Normalización de categorías (UICN, CITES, distribución)  

### 2. Generación de tablas ecológicas

- Estructura jerárquica:
  - Orden → Familia → Especie  
- Cálculo de abundancia por área  
- Totales automáticos  
- Formato listo para exportación (LaTeX / Word)  

### 3. Análisis descriptivo

- Cálculo de:
  - Abundancia total  
  - Riqueza de especies  
  - Número de familias y órdenes  
- Identificación de:
  - Especies dominantes  
  - Áreas con mayor abundancia  

### 4. Automatización de texto técnico

- Generación dinámica por grupo faunístico:
  - Anfibios, reptiles, aves y mamíferos  
- Adaptación a:
  - Presencia/ausencia de datos  
  - Tipo de manejo  
- Redacción automática de:
  - Resultados  
  - Interpretación ecológica  
  - Sección de reubicación  

### 5. Análisis de conservación

- Clasificación UICN  
- Identificación de especies en riesgo (VU, EN, CR)  
- Inclusión en CITES  
- Evaluación de endemismo  

### 6. Visualización

- Gráficos automáticos de:
  - Abundancia por especie  
  - Abundancia por área  
- Escalado dinámico según número de especies  

### 7. Generación de reporte

- Integración de:
  - Texto automático  
  - Tablas  
  - Figuras  
- Exportación mediante **Quarto**  

## 📈 Resultados generados

### 📊 Figuras

- Abundancia por especie  
- Abundancia por área  
- Comparación por tipo de manejo  

### 📋 Tablas

- Registros de fauna por área  
- Estructura taxonómica jerárquica  
- Categorías de conservación (UICN, CITES, distribución)  

### 📝 Texto técnico

- Resultados automatizados por grupo faunístico  
- Sección de reubicación  
- Sección de especies con interés para la conservación  

📄 Informe completo disponible en:  
`/report/report.qmd`

## 📁 Estructura del proyecto
```
├── assets/ # Recursos auxiliares
├── config/ # Configuración del proyecto
│
├── data/
│ ├── raw/ # Datos originales
│ ├── processed/ # Datos limpios
│ └── lookup/ # Tablas de referencia
│
├── outputs/
│ ├── figures/ # Figuras generadas
│ └── tables/ # Tablas exportadas
│
├── scripts/
│ ├── 01_cleaning.R # Limpieza de datos
│ ├── 02_tables.R # Generación de tablas
│ ├── 03_plots.R # Visualizaciones
│ └── Run_all.R # Ejecución completa
│
├── report/
│ └── report.qmd # Reporte en Quarto
│
└── README.md
```

🔁 Reproducibilidad

Este proyecto fue diseñado como un flujo de trabajo completamente reproducible.

Para ejecutar el análisis completo:

```r
source("scripts/Run_all.R")
```

Este script ejecuta de forma secuencial:

- 01_cleaning.py
- 02_tables.py
- 03_plots.py

Una vez finalizado, se puede generar el reporte técnico en PDF con:

```bash
quarto render report/report.qmd
```
