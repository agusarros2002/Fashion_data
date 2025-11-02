"""
==========================================================
Fashion Data - Configuración General del Proyecto
Autor/a: Agustina Arrospide
Versión: 1.5 (Estructura optimizada de Figuras y Logs)
Fecha: 02-11-2025
----------------------------------------------------------
Define rutas base y carpetas principales utilizadas en el
pipeline ETL → KPI → MODEL → EVALUATION → DASHBOARD.
Incluye función universal para guardar figuras y estructura
de logs separada por módulo.
==========================================================
"""

from pathlib import Path
import matplotlib.pyplot as plt

# ==========================================================
# RUTAS PRINCIPALES
# ==========================================================
BASE_DIR = Path(__file__).resolve().parents[1]

# --- Estructura de datos ---
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# --- Carpetas auxiliares ---
REPORT_DIR = BASE_DIR / "report"
MODELS_DIR = BASE_DIR / "models"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# ==========================================================
# SUBCARPETAS ORGANIZADAS DE FIGURAS
# ==========================================================
FIGURES_DIR = REPORT_DIR / "figuras"
FIGURES_ETL = FIGURES_DIR / "etl"
FIGURES_KPI = FIGURES_DIR / "kpi"
FIGURES_MODELS = FIGURES_DIR / "models"   # ✅ ahora se llama "models"
FIGURES_SHAP = FIGURES_DIR / "shap"
FIGURES_MISC = FIGURES_DIR / "otros"      # ✅ opcional, no se crea si no se usa

# ==========================================================
# LOGS (Profesional y organizado)
# ==========================================================
LOGS_DIR = PROCESSED_DIR / "logs"
LOGS_ETL = LOGS_DIR / "etl"
LOGS_KPI = LOGS_DIR / "kpi"
LOGS_ML = LOGS_DIR / "ml"
LOGS_EVAL = LOGS_DIR / "evaluation"
LOGS_DASH = LOGS_DIR / "dashboard"

# ==========================================================
# CREAR TODA LA ESTRUCTURA SI NO EXISTE
# ==========================================================
for folder in [
    RAW_DIR,
    PROCESSED_DIR,
    REPORT_DIR,
    MODELS_DIR,
    NOTEBOOKS_DIR,
    FIGURES_DIR,
    FIGURES_ETL,
    FIGURES_KPI,
    FIGURES_MODELS,
    FIGURES_SHAP,
    LOGS_DIR,
    LOGS_ETL,
    LOGS_KPI,
    LOGS_ML,
    LOGS_EVAL,
    LOGS_DASH,
]:
    folder.mkdir(parents=True, exist_ok=True)

# ==========================================================
# PARÁMETROS GLOBALES
# ==========================================================
RANDOM_STATE = 42
DATE_FORMAT = "%Y-%m-%d"
ENCODING = "utf-8"

# ==========================================================
# ALIAS RETROCOMPATIBLES
# ==========================================================
DATA_RAW = RAW_DIR
DATA_PROCESSED = PROCESSED_DIR
REPORT_FIGURES = FIGURES_DIR

# ==========================================================
# FUNCIÓN UNIVERSAL PARA GUARDAR FIGURAS
# ==========================================================
# ==========================================================
# FUNCIÓN UNIVERSAL PARA GUARDAR FIGURAS (versión final)
# ==========================================================
def save_figure(subfolder: str, filename: str, dpi: int = 300) -> None:
    """
    Guarda la figura actual de matplotlib en la subcarpeta correspondiente
    dentro de report/figuras/.

    Parámetros
    ----------
    subfolder : str
        Nombre de la subcarpeta (etl, kpi, model, evaluacion, shap).
    filename : str
        Nombre del archivo (ej: 'fig_sales_trend.png').
    dpi : int
        Resolución del archivo, por defecto 300.
    """
    folder_map = {
        "etl": FIGURES_ETL,
        "kpi": FIGURES_KPI,
        "model": FIGURES_MODELS,
        "models": FIGURES_MODELS,
        "shap": FIGURES_SHAP,
    }

    subfolder_lower = subfolder.lower().strip()
    target_folder = folder_map.get(subfolder_lower)
    # Asegurar creación de carpeta
    target_folder.mkdir(parents=True, exist_ok=True)

    output_path = target_folder / filename

    try:
        plt.tight_layout()
        plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
        plt.close()
        print(f"✅ Figura guardada en: {output_path}")
    except Exception as e:
        print(f"⚠️ No se pudo guardar la figura '{filename}': {e}")


# ==========================================================
# FUNCIÓN PARA MOSTRAR RUTAS CLAVE
# ==========================================================
def show_paths() -> None:
    """Imprime las rutas clave del proyecto Fashion Data."""
    print("📂 Estructura base de Fashion Data")
    print("=" * 60)
    print(f"BASE_DIR:         {BASE_DIR}")
    print(f"RAW_DIR:          {RAW_DIR}")
    print(f"PROCESSED_DIR:    {PROCESSED_DIR}")
    print(f"REPORT_DIR:       {REPORT_DIR}")
    print(f"FIGURES_DIR:      {FIGURES_DIR}")
    print(f"MODELS_DIR:       {MODELS_DIR}")
    print(f"NOTEBOOKS_DIR:    {NOTEBOOKS_DIR}")
    print(f"LOGS_DIR:         {LOGS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    show_paths()
