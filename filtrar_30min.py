"""
Filtra el archivo JULIO25_VILACEID.xlsx para conservar únicamente
los registros más cercanos a cada intervalo de 30 minutos (HH:00 y HH:30).

Reglas:
  - Selección pura: sin promedios, sin interpolaciones.
  - Se busca la fila cuyo timestamp tiene la menor distancia absoluta
    a cada marca de 30 min.
  - Se conservan TODAS las columnas originales.
"""

import pandas as pd
import datetime

# ── 1. Leer datos ──────────────────────────────────────────────────
df = pd.read_excel("JULIO25_VILACEID.xlsx")

# ── 2. Construir timestamp completo ───────────────────────────────
# Date viene como "01/07/2025 0:00" (texto), Time como "0:00:50" (texto)
# Combinamos para obtener un datetime real.

def parse_datetime(row):
    """Combina Date + Time en un único datetime."""
    date_str = str(row["Date"]).strip()
    time_str = str(row["Time"]).strip()
    # Extraer solo la parte de fecha (dd/mm/yyyy)
    date_part = date_str.split()[0]
    return pd.to_datetime(f"{date_part} {time_str}", format="%d/%m/%Y %H:%M:%S")

df["datetime"] = df.apply(parse_datetime, axis=1)

# ── 3. Generar marcas de 30 min sobre el rango de datos ───────────
start = df["datetime"].min().floor("30min")
end   = df["datetime"].max().ceil("30min")
targets = pd.date_range(start=start, end=end, freq="30min")

# ── 4. Para cada marca, encontrar la fila más cercana ─────────────
selected_indices = set()

for target in targets:
    # Diferencia absoluta respecto a la marca
    diffs = (df["datetime"] - target).abs()
    best_idx = diffs.idxmin()
    selected_indices.add(best_idx)

# ── 5. Extraer filas seleccionadas y ordenar ──────────────────────
result = df.loc[sorted(selected_indices)].copy()

# Eliminar la columna auxiliar 'datetime' para mantener el formato original
result.drop(columns=["datetime"], inplace=True)

# ── 6. Guardar como CSV ──────────────────────────────────────────
output_file = "JULIO25_VILACEID_30min.csv"
result.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Filas originales:  {len(df)}")
print(f"Filas filtradas:   {len(result)}")
print(f"Archivo guardado:  {output_file}")
print(f"\nPrimeras 10 filas del resultado:")
print(result.head(10).to_string(index=False))
