# ===========================================
# CLEANING
# ===========================================

import pandas as pd
from pathlib import Path

# ===========================================
# RUTAS
# ===========================================

# Detecta automáticamente la raíz del proyecto
try:
    BASE_DIR = Path(__file__).resolve().parents[1]
except NameError:
    BASE_DIR = Path.cwd()

INPUT_PATH = BASE_DIR / "data/raw/fauna_marzo_2026.csv"
OUTPUT_PATH = BASE_DIR / "data/processed/fauna_clean.csv"
LOOKUP_PATH = BASE_DIR / "data/lookup/species_info.csv"

# ===========================================
# VALIDACIÓN DE ARCHIVO
# ===========================================

if not INPUT_PATH.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {INPUT_PATH}")

if not LOOKUP_PATH.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {LOOKUP_PATH}")

# ===========================================
# CARGA DE DATOS
# ===========================================

df = pd.read_csv(INPUT_PATH)
species_info = pd.read_csv(LOOKUP_PATH, sep=";")

print("Archivo principal cargado correctamente")
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

print("Archivo de especies cargado correctamente")
print(f"Filas: {species_info.shape[0]} | Columnas: {species_info.shape[1]}")

# ===========================================
# VALIDACIÓN DE COLUMNAS
# ===========================================

columnas_esperadas = [
    "Id_registro",
    "Fecha",
    "Proyecto",
    "Area",
    "Actividad",
    "Manejo",
    "Clase",
    "Especie",
    "Nombre_comun",
    "Abundancia",
    "Estado",
    "Reubicado"
]

faltantes = [col for col in columnas_esperadas if col not in df.columns]

if faltantes:
    raise ValueError(f"Faltan columnas en el dataset: {faltantes}")

print("Columnas validadas")

# ===========================================
# LIMPIEZA BÁSICA
# ===========================================

# eliminar espacios en texto
df.columns = df.columns.str.strip()

# quitar espacios en strings
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Clave de unión
df["Especie"] = df["Especie"].str.lower().str.strip()
species_info["Especie"] = species_info["Especie"].str.lower().str.strip()

# ===========================================
# TIPOS DE DATOS
# ===========================================

# Fecha
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

# Abundancia
df["Abundancia"] = pd.to_numeric(df["Abundancia"], errors="coerce")

# ===========================================
# VALIDACIONES CRÍTICAS
# ===========================================

# valores nulos clave
if df["Abundancia"].isna().any():
    print("Hay valores nulos en Abundancia")

if df["Fecha"].isna().any():
    print("Hay fechas inválidas")

# abundancia negativa (error grave)
if (df["Abundancia"] < 0).any():
    raise ValueError("Hay valores negativos en Abundancia")

# ===========================================
# ESTANDARIZACIÓN
# ===========================================

# texto consistente
df["Manejo"] = df["Manejo"].str.capitalize()
df["Clase"] = df["Clase"].str.capitalize()

# renombrar columnas 
species_info.columns = [
    "Especie",
    "Orden",
    "Familia",
    "CITES",
    "IUCN",
    "Distribucion"
]

# enriquecer info_spp
df = df.merge(
    species_info,
    on="Especie",
    how="left"
)

# validación post-merge
missing_iucn = df["IUCN"].isna().sum()

if missing_iucn > 0:
    print(f"{missing_iucn} registros sin información de IUCN")

coverage = 1 - (missing_iucn / len(df))
print(f" Cobertura de enriquecimiento: {coverage:.2%}")


# formato nombre cientifico
def format_species(text):
    if pd.isna(text):
        return text
    
    parts = text.split()
    
    if len(parts) >= 2:
        return parts[0].capitalize() + " " + parts[1].lower()
    
    return text

df["Especie"] = df["Especie"].apply(format_species)

# ===========================================
# EXPORTAR DATA LIMPIA
# ===========================================

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print(f"Dataset limpio guardado en: {OUTPUT_PATH}")

