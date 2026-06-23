import pandas as pd
import numpy as np

# ============================================================
# 1. CARGA DE DATOS
# ============================================================
print("Cargando datos...")

# --- Villaceid ---
df_vc = pd.read_excel("JULIO25_VILACEID.xlsx")
# Date: "01/07/2025 0:00", Time: "0:00:50"
# Combinar Date (solo fecha) + Time para crear datetime completo
df_vc["Date_str"] = df_vc["Date"].astype(str).str.strip()
df_vc["Time_str"] = df_vc["Time"].astype(str).str.strip()
# Extraer solo la parte de fecha del campo Date (puede tener " 0:00" al final)
df_vc["fecha"] = df_vc["Date_str"].str.split(" ").str[0]
df_vc["datetime"] = pd.to_datetime(df_vc["fecha"] + " " + df_vc["Time_str"], format="%d/%m/%Y %H:%M:%S")
df_vc = df_vc[["datetime", "Temperature (C)"]].rename(columns={"Temperature (C)": "Temp_Villaceid"})
df_vc = df_vc.set_index("datetime").sort_index()
print(f"  Villaceid: {len(df_vc)} registros, rango: {df_vc.index.min()} -> {df_vc.index.max()}")

# --- Villayuste ---
df_vy = pd.read_excel("JULIO25_VILLAYUSTE.xlsx")
# Date: "2025-07-01" o "2025-07-31 00:00:00", Time: "0:04:00"
df_vy["Date_str"] = df_vy["Date"].astype(str).str.strip()
df_vy["Time_str"] = df_vy["Time"].astype(str).str.strip()
# Extraer solo la parte de fecha
df_vy["fecha"] = df_vy["Date_str"].str.split(" ").str[0]
df_vy["datetime"] = pd.to_datetime(df_vy["fecha"] + " " + df_vy["Time_str"], format="%Y-%m-%d %H:%M:%S")
df_vy = df_vy[["datetime", "Temperature (C)"]].rename(columns={"Temperature (C)": "Temp_Villayuste"})
df_vy = df_vy.set_index("datetime").sort_index()
print(f"  Villayuste: {len(df_vy)} registros, rango: {df_vy.index.min()} -> {df_vy.index.max()}")

# ============================================================
# 2. RESAMPLING A 30 MINUTOS (NEAREST NEIGHBOR)
# ============================================================
print("\nResampleando a intervalos de 30 minutos (nearest neighbor)...")

# Crear la grilla de 30 minutos que cubra ambos datasets
inicio = max(df_vc.index.min(), df_vy.index.min()).ceil("30min")
fin = min(df_vc.index.max(), df_vy.index.max()).floor("30min")
grilla_30min = pd.date_range(start=inicio, end=fin, freq="30min")
print(f"  Grilla: {grilla_30min[0]} -> {grilla_30min[-1]} ({len(grilla_30min)} marcas)")

# Nearest neighbor: para cada marca de 30 min, encontrar el dato real más cercano
# Usamos merge_asof con direction='nearest'
df_grilla = pd.DataFrame({"datetime": grilla_30min})

# Villaceid - nearest
vc_reset = df_vc.reset_index()
vc_nearest = pd.merge_asof(
    df_grilla.sort_values("datetime"),
    vc_reset.sort_values("datetime"),
    on="datetime",
    direction="nearest"
)

# Villayuste - nearest
vy_reset = df_vy.reset_index()
vy_nearest = pd.merge_asof(
    df_grilla.sort_values("datetime"),
    vy_reset.sort_values("datetime"),
    on="datetime",
    direction="nearest"
)

# Combinar
df_sync = pd.DataFrame({
    "datetime": grilla_30min,
    "Temp_Villaceid": vc_nearest["Temp_Villaceid"].values,
    "Temp_Villayuste": vy_nearest["Temp_Villayuste"].values
})

# Eliminar filas con NaN
antes = len(df_sync)
df_sync = df_sync.dropna(subset=["Temp_Villaceid", "Temp_Villayuste"])
print(f"  Registros sincronizados: {len(df_sync)} (eliminados {antes - len(df_sync)} con NaN)")

# ============================================================
# 3. DETECCIÓN DE EVENTOS (Villaceid < Villayuste)
# ============================================================
print("\nDetectando eventos térmicos (Villaceid < Villayuste)...")

df_sync["evento_activo"] = df_sync["Temp_Villaceid"] < df_sync["Temp_Villayuste"]
df_sync["diff_temp"] = df_sync["Temp_Villayuste"] - df_sync["Temp_Villaceid"]

# Identificar bloques contiguos: cada vez que cambia el estado, es un nuevo grupo
df_sync["cambio_grupo"] = df_sync["evento_activo"].ne(df_sync["evento_activo"].shift()).cumsum()

# Filtrar solo los grupos donde la condición se cumple
eventos_activos = df_sync[df_sync["evento_activo"]].copy()

if len(eventos_activos) == 0:
    print("No se detectaron eventos térmicos.")
else:
    # Agrupar por bloque continuo
    resultados = []
    for id_grupo, grupo in eventos_activos.groupby("cambio_grupo"):
        inicio_ev = grupo["datetime"].iloc[0]
        fin_ev = grupo["datetime"].iloc[-1]
        duracion = (fin_ev - inicio_ev)
        duracion_horas = duracion.total_seconds() / 3600.0
        diff_max = grupo["diff_temp"].max()

        resultados.append({
            "ID_Evento": len(resultados) + 1,
            "Inicio": inicio_ev,
            "Fin": fin_ev,
            "Duracion_Horas": round(duracion_horas, 2),
            "Diferencia_Temp_Max": round(diff_max, 2)
        })

    df_resultados = pd.DataFrame(resultados)

    print(f"\n  [OK] Se detectaron {len(df_resultados)} eventos térmicos.")
    print(f"\n  Resumen:")
    print(f"    - Duración media: {df_resultados['Duracion_Horas'].mean():.2f} horas")
    print(f"    - Duración máxima: {df_resultados['Duracion_Horas'].max():.2f} horas")
    print(f"    - Diferencia de temp. máx. global: {df_resultados['Diferencia_Temp_Max'].max():.2f} °C")

    # ============================================================
    # 4. EXPORTAR A EXCEL
    # ============================================================
    output_file = "Eventos_Termicos_Julio2025.xlsx"
    df_resultados.to_excel(output_file, index=False, sheet_name="Eventos")
    print(f"\n  [OK] Archivo guardado: {output_file}")
    print(f"\nPrimeros 10 eventos:")
    print(df_resultados.head(10).to_string(index=False))
