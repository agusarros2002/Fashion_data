"""
==========================================================
Fashion Data - Evaluación y Visualizaciones
Autor/a: Agustina Arrospide
Versión: 1.8 (rutas ML corregidas + consistencia figuras)
==========================================================
"""

import logging
import warnings
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.config import PROCESSED_DIR, save_figure, LOGS_EVAL

# ----------------------------------------------------------
# Configuración general
# ----------------------------------------------------------
LOG_FILE = LOGS_EVAL / "evaluation_log.txt"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Evitar mensajes de Matplotlib sobre "categorical units"
warnings.filterwarnings("ignore", message="Using categorical units")
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

sns.set(style="whitegrid", palette="crest", context="talk")

# ----------------------------------------------------------
# Gráficos de ETL
# ----------------------------------------------------------
def plot_etl_quality() -> None:
    """Genera gráficos de calidad de datos del ETL."""
    path = PROCESSED_DIR / "fashion_sales_clean.csv"
    if not path.exists():
        logger.warning("⚠️ No se encontró fashion_sales_clean.csv.")
        return

    df = pd.read_csv(path)

    if "purchase_amount_usd" in df.columns:
        plt.figure(figsize=(8, 4))
        sns.histplot(df["purchase_amount_usd"], bins=30, kde=True)
        plt.title("Distribución del Monto de Compra (USD)")
        plt.xlabel("Monto de compra (USD)")
        plt.ylabel("Frecuencia")
        plt.tight_layout()
        save_figure("etl", "fig_purchase_distribution.png")

    if "payment_method" in df.columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(
            y="payment_method",
            data=df,
            order=df["payment_method"].value_counts().index
        )
        plt.title("Frecuencia de Métodos de Pago")
        plt.xlabel("Cantidad de transacciones")
        plt.ylabel("Método de pago")
        plt.tight_layout()
        save_figure("etl", "fig_payment_methods.png")

# ----------------------------------------------------------
# Gráficos de KPI
# ----------------------------------------------------------
def plot_kpis() -> None:
    """Genera visualización de la evolución mensual de ventas."""
    sales = PROCESSED_DIR / "kpi" / "kpi_sales.csv"

    if not sales.exists():
        logger.warning("⚠️ No se encontró el archivo de KPI de ventas.")
        return

    df_sales = pd.read_csv(sales)

    # Asegurar orden cronológico de los meses
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Eliminar filas con meses no válidos o nulos
    df_sales = df_sales[df_sales["purchase_month"].isin(month_order)]

    # Asegurar dtype categórico ordenado
    df_sales["purchase_month"] = pd.Categorical(
        df_sales["purchase_month"],
        categories=month_order,
        ordered=True
    )


    plt.figure(figsize=(8, 4))
    sns.lineplot(x="purchase_month", y="total_ventas_usd", data=df_sales, marker="o")
    plt.title("Evolución Mensual de Ventas (USD)")
    plt.xlabel("Mes")
    plt.ylabel("Ventas Totales (USD)")
    plt.tight_layout()
    save_figure("kpi", "fig_sales_trend.png")

    logger.info("✅ Gráfico de KPI de ventas generado correctamente.")

# ----------------------------------------------------------
# Gráficos de modelos ML
# ----------------------------------------------------------
def plot_models() -> None:
    """Genera visualizaciones comparativas de modelos ML."""
    reg = PROCESSED_DIR / "ml" / "ml_results_regression.csv"
    if reg.exists():
        df = pd.read_csv(reg)
        plt.figure(figsize=(8, 4))
        df["model"] = df["model"].astype("category")
        sns.barplot(x="model", y="RMSE", data=df)
        plt.title("Comparativa RMSE - Modelos de Regresión")
        plt.xlabel("Modelo")
        plt.ylabel("RMSE")
        plt.tight_layout()
        save_figure("models", "fig_rmse_regression.png")
    else:
        logger.warning("⚠️ No se encontró ml_results_regression.csv")

    clf = PROCESSED_DIR / "ml" / "ml_results_classification.csv"
    if clf.exists():
        df = pd.read_csv(clf)
        plt.figure(figsize=(8, 4))
        df["model"] = df["model"].astype("category")
        sns.barplot(x="model", y="f1_macro", data=df)
        plt.title("Comparativa F1 Macro - Modelos de Clasificación")
        plt.xlabel("Modelo")
        plt.ylabel("F1 Macro")
        plt.tight_layout()
        save_figure("models", "fig_f1_classification.png")
    else:
        logger.warning("⚠️ No se encontró ml_results_classification.csv")

# ----------------------------------------------------------
# Ejecución principal
# ----------------------------------------------------------
def run_evaluation() -> None:
    """Ejecuta todas las visualizaciones del proyecto."""
    logger.info("🎨 Generando visualizaciones del proyecto...")
    plot_etl_quality()
    plot_kpis()
    plot_models()
    logger.info("✅ Visualizaciones completadas correctamente.")


if __name__ == "__main__":
    run_evaluation()
