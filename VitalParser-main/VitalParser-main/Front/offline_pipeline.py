from datetime import datetime

# IMPORTA AQUÍ TUS FUNCIONES REALES
from utils_offline import merge_selected_csv, calcular_intervalos_tiempo, trim_algorithms_csv_by_time, datetime_to_unix
import vitaldb
import os
from Algorithms.check_availability import check_availability
from Algorithms.shock_index import ShockIndex
from Algorithms.driving_pressure import DrivingPressure
from Algorithms.dynamic_compliance import DynamicCompliance
from Algorithms.rox_index import RoxIndex
from Algorithms.temp_comparison import TempComparison
from Algorithms.cardiac_output import CardiacOutput
from Algorithms.systemic_vascular_resistance import SystemicVascularResistance
from Algorithms.cardiac_power_output import CardiacPowerOutput
from Algorithms.effective_arterial_elastance import EffectiveArterialElastance
from Algorithms.heart_rate_variability import HeartRateVariability

def run_offline_pipeline(
    vital_path: str,
    algoritmos: list[str],
    constantes: list[str],
    *,
    vital_alg_out: str = "./Offline/offline_algoritmos.vital",
    vital_const_out_path: str = "./Offline/offline_constantes.vital",
) -> dict:
    """
    Ejecuta todo el flujo offline y devuelve rutas de salida.
    """

    # -------------------------------
    # 1) .vital de algoritmos
    # -------------------------------
    vf = vitaldb.VitalFile(vital_path)
    tracks = vf.get_track_names()
    algoritmos = check_availability(tracks)
    results = {}
    if algoritmos:
        for algorithm in algoritmos:
            if algorithm == 'Shock Index':
                results['Shock Index'] = ShockIndex(vf).values
            elif algorithm == 'Driving Pressure':
                results['Driving Pressure'] = DrivingPressure(vf).values
            elif algorithm == 'Dynamic Compliance':
                results['Dynamic Compliance'] = DynamicCompliance(vf).values
            elif algorithm == 'ROX Index':
                results['ROX Index'] = RoxIndex(vf).values
            elif algorithm == 'Temp Comparison':
                results['Temp Comparison'] = TempComparison(vf).values
            elif algorithm == 'Cardiac Output':
                results['Cardiac Output'] = CardiacOutput(vf).values
            elif algorithm == 'Systemic Vascular Resistance':
                results['Systemic Vascular Resistance'] = SystemicVascularResistance(vf).values
            elif algorithm == 'Cardiac Power Output':
                results['Cardiac Power Output'] = CardiacPowerOutput(vf).values
            elif algorithm == 'Effective Arterial Elastance':
                results['Effective Arterial Elastance'] = EffectiveArterialElastance(vf).values

        # Crear un nuevo VitalFile para los algoritmos
        output_dir = "./CSV"  # o la carpeta que estés usando
        os.makedirs(output_dir, exist_ok=True)

        for algo_name, df_algo in results.items():
            # Copia para no tocar el original
            df_out = df_algo.copy()

            # Renombrar columna timestamp -> time si existe
            if "timestamp" in df_out.columns:
                df_out = df_out.rename(columns={"timestamp": "time"})

            # Nombre de archivo: p.ej. "Shock Index" -> "ShockIndex.csv"
            safe_name = algo_name.replace(" ", "")
            csv_path = os.path.join(output_dir, f"{safe_name}.csv")

            # Guardar solo las dos columnas (time + valor)
            # Si el DataFrame tiene más columnas, puedes limitarlo así:
            # cols = ["time"] + [c for c in df_out.columns if c != "time"]
            # df_out = df_out[cols]

            df_out.to_csv(csv_path, index=False)
            print(f"Guardado CSV de {algo_name} en: {csv_path}")


    else:
        vital_alg_out = None

    # -------------------------------
    # 2) .vital de constantes
    # -------------------------------
    vital_const_out = vitaldb.VitalFile(vital_path, track_names=constantes)
    vital_const_out.to_vital(vital_const_out_path, compresslevel=1)



    # (opcional) borrar vital_const_trimmed más adelante

    return {
        "alg_vital_path": vital_alg_out,
        "const_vital_path": vital_const_out_path ,
    }
