# ===========================================
# TABLAS
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

INPUT_PATH = BASE_DIR / "data/processed/fauna_clean.csv"
OUTPUT_GENERAL = BASE_DIR / "outputs/tables/tabla_clase_manejo.csv"
OUTPUT_DETALLE = BASE_DIR / "outputs/tables/tabla_detalle.csv"

# ===========================================
# CARGA
# ===========================================

df = pd.read_csv(INPUT_PATH)

# ===========================================
# VALIDACIÓN
# ===========================================

if df.empty:
    raise ValueError("El dataset está vacío")

# ===========================================
# TABLA GENERAL
# ===========================================

# Sumar abundancia por clase y tipo de manejo
resumen = (
    df
    .groupby(["Clase", "Manejo"])["Abundancia"]
    .sum()
    .reset_index(name="N")
)

# ===========================================
# PIVOT
# ===========================================

tabla = (
    resumen
    .pivot_table(
        index="Clase",
        columns="Manejo",
        values="N",
        fill_value=0
    )
    .reset_index()
)

# asegurar columnas
for col in ["Ahuyentamiento", "Rescate"]:
    if col not in tabla.columns:
        tabla[col] = 0

# ===========================================
# TOTAL
# ===========================================

tabla["Total"] = tabla["Ahuyentamiento"] + tabla["Rescate"]

# Fila total general
fila_total = pd.DataFrame({
    "Clase": ["Total"],
    "Ahuyentamiento": [tabla["Ahuyentamiento"].sum()],
    "Rescate": [tabla["Rescate"].sum()],
    "Total": [tabla["Total"].sum()]
})

tabla = pd.concat([tabla, fila_total], ignore_index=True)

# Convertir a enteros
for col in ["Ahuyentamiento", "Rescate", "Total"]:
    tabla[col] = tabla[col].astype(int)

# ===========================================
# ORDEN TAXONÓMICO
# ===========================================

orden = ["Amphibia", "Reptilia", "Aves", "Mammalia"]

tabla["Clase"] = pd.Categorical(
    tabla["Clase"],
    categories=orden + ["Total"],
    ordered=True
)

tabla = tabla.sort_values("Clase")

# ===========================================
# EXPORTAR
# ===========================================

OUTPUT_GENERAL.parent.mkdir(parents=True, exist_ok=True)

tabla.to_csv(OUTPUT_GENERAL, index=False)

print("Tabla generada correctamente")
print(tabla)

# ===========================================
# TABLA DETALLADA
# ===========================================

def build_tabla_detalle(df):

    if df.empty:
        print("Sin datos para tabla detallada")
        return None

    # ===========================================
    # METADATA POR ESPECIE
    # ===========================================

    meta = (
        df
        .drop_duplicates(subset=["Especie"])
        .set_index("Especie")[
            ["Nombre_comun", "CITES", "IUCN", "Distribucion"]
        ]
    )

    # ===========================================
    # AGRUPACIÓN BASE
    # ===========================================

    conteos = (
        df
        .groupby([
            "Manejo",
            "Clase",
            "Orden",
            "Familia",
            "Especie",
            "Area"
        ])["Abundancia"]
        .sum()
        .reset_index()
    )

    # ===========================================
    # PIVOT DE ÁREAS
    # ===========================================

    tabla = (
        conteos
        .pivot_table(
            index=[
                "Manejo",
                "Clase",
                "Orden",
                "Familia",
                "Especie"
            ],
            columns="Area",
            values="Abundancia",
            fill_value=0
        )
        .reset_index()
    )

    tabla.columns.name = None

    # ===========================================
    # MERGE METADATA
    # ===========================================

    tabla = tabla.merge(
        meta,
        on="Especie",
        how="left"
    )
    
    # =========================
    # NORMALIZAR CATEGORÍAS
    # =========================
    
    # CITES
    map_cites = {
        "Apéndice I": "I",
        "Apéndice II": "II",
        "Apéndice III": "III"
    }
    # IUCN
    map_iucn = {
        "Preocupación Menor (LC)": "LC",
        "Casi Amenazado (NT)": "NT",
        "Vulnerable (VU)": "VU",
        "En Peligro (EN)": "EN",
        "En Peligro Critico (CR)": "CR",
        "Datos insuficientes (DD)": "DD",
        "No Evaluado (NE)": "NE"
    }
    
    #Distribución
    map_dist = {
        "Endémica": "EN",
        "Casi endémica": "CE",
        "Restringida": "RE",
        "Residente": "RE",
        "Cosmopolita": "C"
    }
    
    tabla["IUCN"] = tabla["IUCN"].replace(map_iucn)
    tabla["Distribucion"] = tabla["Distribucion"].replace(map_dist)
    
    # CITES → NA como guión largo
    tabla["CITES"] = tabla["CITES"].map(map_cites).fillna("—")

    # ===========================================
    # IDENTIFICAR ÁREAS
    # ===========================================

    cols_fijas = [
        "Manejo","Clase","Orden","Familia","Especie",
        "Nombre_comun","CITES","IUCN","Distribucion"
    ]

    areas = [c for c in tabla.columns if c not in cols_fijas]

    # ===========================================
    # TOTAL POR FILA
    # ===========================================

    tabla["Total"] = tabla[areas].sum(axis=1)

    # ===========================================
    # ORDENAR
    # ===========================================

    tabla = tabla.sort_values(
        by=["Clase","Manejo","Orden","Familia","Especie"]
    )

    # ===========================================
    # JERARQUÍA TAXONÓMICA
    # ===========================================

    tabla_partes = []

    for (manejo, clase), df_sub in tabla.groupby(["Manejo","Clase"]):

        for orden in df_sub["Orden"].dropna().unique():

            sub_ord = df_sub[df_sub["Orden"] == orden]

            # -------- ORDEN --------
            fila_orden = pd.DataFrame({
                "Taxon":[f"\\textbf{{Orden {orden}}}"],
                "Nombre_comun":[""],
                "CITES":[""],
                "IUCN":[""],
                "Distribucion":[""],
                **{a:"" for a in areas},
                "Total":[""]
            })

            tabla_temp = fila_orden.copy()

            for familia in sub_ord["Familia"].dropna().unique():

                sub_fam = sub_ord[sub_ord["Familia"] == familia]

                # -------- FAMILIA --------
                fila_fam = pd.DataFrame({
                    "Taxon":[f"\\hspace{{3mm}}\\textbf{{Familia {familia}}}"],
                    "Nombre_comun":[""],
                    "CITES":[""],
                    "IUCN":[""],
                    "Distribucion":[""],
                    **{a:"" for a in areas},
                    "Total":[""]
                })

                tabla_temp = pd.concat([tabla_temp, fila_fam], ignore_index=True)

                # -------- ESPECIES --------
                especies = sub_fam.copy()

                especies["Taxon"] = "\\hspace{6mm}\\textit{" + especies["Especie"] + "}"

                especies = especies[
                    ["Taxon","Nombre_comun","CITES","IUCN","Distribucion"]
                    + areas + ["Total"]
                ]

                tabla_temp = pd.concat([tabla_temp, especies], ignore_index=True)

            tabla_partes.append(tabla_temp)

    tabla_final = pd.concat(tabla_partes, ignore_index=True)

    # ===========================================
    # TOTAL GENERAL + RESUMEN TAXONÓMICO
    # ===========================================
    
    nums = tabla[areas].apply(pd.to_numeric, errors="coerce")
    totales = nums.sum()
    
    # resumen taxonómico
    n_ordenes = df["Orden"].nunique()
    n_familias = df["Familia"].nunique()
    n_especies = df["Especie"].nunique()
    
    def plural(n, singular, plural):
        return singular if n == 1 else plural

    texto_total = (
        f"Total: "
        f"{n_ordenes} {plural(n_ordenes, 'orden', 'órdenes')}, "
        f"{n_familias} {plural(n_familias, 'familia', 'familias')}, "
        f"{n_especies} {plural(n_especies, 'especie', 'especies')}"
    )
    
    # UNA sola fila final
    total_row = pd.DataFrame({
        "Taxon":[texto_total],
        "Nombre_comun":[""],
        "CITES":[""],
        "IUCN":[""],
        "Distribucion":[""],
        **totales.to_dict(),
        "Total":[int(totales.sum())]
    })
    
    tabla_final = pd.concat([tabla_final, total_row], ignore_index=True)
    
    # ===========================================
    # LIMPIEZA VISUAL
    # ===========================================
    
    # identificar filas de especies (las que tienen datos reales)
    mask_especies = tabla_final["Nombre_comun"] != ""
    mask_total = tabla_final["Taxon"].str.contains("Total", na=False)
    
    for col in areas + ["Total"]:

      tabla_final[col] = pd.to_numeric(tabla_final[col], errors="coerce")
      tabla_final[col] = tabla_final[col].astype(object)
      
      # especies → valores normales
      tabla_final.loc[mask_especies, col] = (
          tabla_final.loc[mask_especies, col]
          .fillna(0)
          .astype(int)
          .astype(str)
          .replace("0", "—")
      )
      
      # totales → SIEMPRE mostrar número
      tabla_final.loc[mask_total, col] = (
          tabla_final.loc[mask_total, col]
          .fillna(0)
        .astype(int)
        .astype(str)
      )
      
      # jerárquicas → vacío
      tabla_final.loc[~mask_especies & ~mask_total, col] = ""
    
    return tabla_final

# ===========================================
# EXPORTAR
# ===========================================

tabla_detalle = build_tabla_detalle(df)

OUTPUT_DETALLE.parent.mkdir(parents=True, exist_ok=True)

tabla_detalle.to_csv(OUTPUT_DETALLE, index=False)

print("Tabla detallada generada")
print(tabla_detalle.head())

# ===========================================
# TABLA DE INDICADORES 
# ===========================================
def fmt_pct_val(num, den):
    if den == 0:
        return "0%"
    pct = (num / den) * 100
    pct_fmt = f"{pct:.1f}".rstrip('0').rstrip('.') + "%"
    return f"{pct_fmt} ({int(num)} / {int(den)})"
  
def build_tabla_indicadores(df_input):
    if df_input.empty:
        return None

    # Totales por tipo de Manejo
    ahuyentados = df_input.loc[df_input["Manejo"] == "Ahuyentamiento", "Abundancia"].sum()
    rescatados = df_input.loc[df_input["Manejo"] == "Rescate", "Abundancia"].sum()
    
    # Filtrar solo para el análisis de Rescates (Mortalidad y Reubicación)
    df_rescates = df_input[df_input["Manejo"] == "Rescate"]
    
    reubicados_res = df_rescates.loc[df_rescates["Reubicado"] == "si", "Abundancia"].sum()
    vivos_res = df_rescates.loc[df_rescates["Estado"] == "vivo", "Abundancia"].sum()
    muertos_res = df_rescates.loc[df_rescates["Estado"] == "muerto", "Abundancia"].sum()

    # Cálculo de Indicadores
    # I1: Tasa de Permanencia/Rescate (Rescatados / Ahuyentados)
    ind1 = (rescatados / ahuyentados * 100) if ahuyentados > 0 else 0
    
    # I2: Éxito Reubicación: (Reubicados / Rescatados)
    ind2 = (reubicados_res / rescatados * 100) if rescatados > 0 else 0
    
    # I3: Mortalidad: (Muertos / Vivos del grupo rescate)
    ind3 = (muertos_res / rescatados * 100) if vivos_res > 0 else 0

    # Estructura con Descripciones de Cumplimiento
    data = [
        {
            "Indicador": "Efectividad de Ahuyentamiento",
            "Descripción": "Rescatados / Ahuyentados",
            "Resultado": fmt_pct_val(rescatados, ahuyentados),
            "Meta": "< 20%",
            "Cumple": "Sí" if ind1 < 20 else "No"
        },
        {
            "Indicador": "Éxito de Reubicación",
            "Descripción": "Reubicados / Rescatados",
            "Resultado": fmt_pct_val(reubicados_res, rescatados),
            "Meta": "> 95%",
            "Cumple": "Sí" if ind2 > 95 else "No"
        },
        {
            "Indicador": "Tasa de Mortalidad",
            "Descripción": "Muertos / Rescatados",
            "Resultado": fmt_pct_val(muertos_res, rescatados),
            "Meta": "< 5%",
            "Cumple": "Sí" if ind3 < 5 else "No"
        }
    ]
    
    return pd.DataFrame(data)

# ===========================================
# EXPORTAR
# ===========================================
OUTPUT_INDICADORES = BASE_DIR / "outputs/tables/tabla_indicadores.csv"
tabla_indicadores = build_tabla_indicadores(df)

if tabla_indicadores is not None:
    tabla_indicadores.to_csv(OUTPUT_INDICADORES, index=False)
    print("Tabla de indicadores generada.")
