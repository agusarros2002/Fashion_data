"""
==========================================================
Fashion Data - Generación de KPIs
Autor/a: Agustina Arrospide
Versión: 1.4 (PEP 8 + config.py + Logging unificado)
Fecha: 01-11-2025
----------------------------------------------------------
Descripción:
    Calcula indicadores clave (KPIs) del dataset limpio
    'fashion_sales_clean.csv' para alimentar dashboards.

Incluye:
    - KPI de ventas por mes y segmento
    - KPI por método de pago
    - KPI de satisfacción
    - KPI de clientes
    - Resumen general
==========================================================
"""

import logging
import pandas as pd
from pathlib import Path
from src.config import DATA_PROCESSED, LOGS_KPI

# ----------------------------------------------------------
# Configuración general
# ----------------------------------------------------------
INPUT_PATH = DATA_PROCESSED / "fashion_sales_clean.csv"
OUTPUT_DIR = DATA_PROCESSED / "kpi"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_KPI / "kpi_log.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ----------------------------------------------------------
# Funciones principales de cálculo de KPIs
# ----------------------------------------------------------
def load_clean_data(path: Path) -> pd.DataFrame:
    """Carga el dataset limpio."""
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el dataset en {path}")

    logger.info("Cargando dataset limpio desde: %s", path)
    df = pd.read_csv(path)
    logger.info("Dataset cargado correctamente: %d filas, %d columnas", *df.shape)
    return df


def generate_sales_kpi(df: pd.DataFrame, output_dir: Path) -> None:
    """Genera KPI de ventas por año, mes y segmento."""
    logger.info("Generando KPI de ventas...")

    required_cols = {"purchase_year", "purchase_month", "ticket_segment"}
    if not required_cols.issubset(df.columns):
        logger.warning("Columnas necesarias para KPI de ventas no encontradas.")
        return

    kpi_sales = (
        df.groupby(list(required_cols), as_index=False)
        .agg(
            total_ventas_usd=("purchase_amount_usd", "sum"),
            promedio_ticket_usd=("purchase_amount_usd", "mean"),
            cantidad_transacciones=("purchase_amount_usd", "count"),
        )
        .sort_values(by=["purchase_year", "purchase_month"])
    )

    output_path = output_dir / "kpi_sales.csv"
    kpi_sales.to_csv(output_path, index=False)
    logger.info("KPI de ventas guardado en: %s", output_path)


def generate_payment_kpi(df: pd.DataFrame, output_dir: Path) -> None:
    """Genera KPI por método de pago."""
    logger.info("Generando KPI de método de pago...")

    if "payment_method" not in df.columns:
        logger.warning("Columna 'payment_method' no encontrada.")
        return

    kpi_payment = (
        df.groupby("payment_method", as_index=False)
        .agg(
            total_ventas_usd=("purchase_amount_usd", "sum"),
            transacciones=("payment_method", "count"),
        )
    )

    kpi_payment["porcentaje"] = (
        (kpi_payment["transacciones"] / kpi_payment["transacciones"].sum()) * 100
    ).round(2)

    output_path = output_dir / "kpi_payment.csv"
    kpi_payment.to_csv(output_path, index=False)
    logger.info("KPI de método de pago guardado en: %s", output_path)


def generate_satisfaction_kpi(df: pd.DataFrame, output_dir: Path) -> None:
    """Genera KPI de satisfacción por mes y nivel."""
    logger.info("Generando KPI de satisfacción...")

    required_cols = {"purchase_year", "purchase_month", "satisfaction_level"}
    if not required_cols.issubset(df.columns):
        logger.warning("Columnas necesarias para KPI de satisfacción no encontradas.")
        return

    kpi_satisfaction = (
        df.groupby(list(required_cols), as_index=False)
        .agg(
            rating_promedio=("review_rating", "mean"),
            cantidad_clientes=("review_rating", "count"),
        )
    )

    output_path = output_dir / "kpi_satisfaction.csv"
    kpi_satisfaction.to_csv(output_path, index=False)
    logger.info("KPI de satisfacción guardado en: %s", output_path)


def generate_customer_kpi(df: pd.DataFrame, output_dir: Path) -> None:
    """Genera KPI de clientes (frecuencia y gasto promedio)."""
    logger.info("Generando KPI de clientes...")

    if "customer_reference_id" not in df.columns:
        logger.warning("Columna 'customer_reference_id' no encontrada.")
        return

    kpi_customer = (
        df.groupby("customer_reference_id", as_index=False)
        .agg(
            total_gasto_usd=("purchase_amount_usd", "sum"),
            compras=("purchase_amount_usd", "count"),
            rating_promedio=("review_rating", "mean"),
        )
    )

    kpi_customer["ticket_medio_usd"] = (
        kpi_customer["total_gasto_usd"] / kpi_customer["compras"]
    ).round(2)

    output_path = output_dir / "kpi_customer.csv"
    kpi_customer.to_csv(output_path, index=False)
    logger.info("KPI de clientes guardado en: %s", output_path)


def print_summary(df: pd.DataFrame) -> None:
    """Imprime resumen global de indicadores."""
    summary = {
        "Total registros": len(df),
        "Clientes únicos": (
            df["customer_reference_id"].nunique()
            if "customer_reference_id" in df.columns
            else "N/A"
        ),
        "Ticket medio (USD)": (
            round(df["purchase_amount_usd"].mean(), 2)
            if "purchase_amount_usd" in df.columns
            else "N/A"
        ),
        "Rating promedio": (
            round(df["review_rating"].mean(), 2)
            if "review_rating" in df.columns
            else "N/A"
        ),
        "Ventas totales (USD)": (
            round(df["purchase_amount_usd"].sum(), 2)
            if "purchase_amount_usd" in df.columns
            else "N/A"
        ),
    }

    logger.info("Resumen general de KPIs:")
    for key, value in summary.items():
        logger.info("  %s: %s", key, value)


# ----------------------------------------------------------
# Función principal del módulo
# ----------------------------------------------------------
def run_kpi() -> None:
    """Ejecuta el pipeline completo de generación de KPIs."""
    logger.info("Iniciando generación de KPIs - Fashion Data")

    if not INPUT_PATH.exists():
        logger.error("No se encontró el dataset limpio: %s", INPUT_PATH)
        return

    df = load_clean_data(INPUT_PATH)
    generate_sales_kpi(df, OUTPUT_DIR)
    generate_payment_kpi(df, OUTPUT_DIR)
    generate_satisfaction_kpi(df, OUTPUT_DIR)
    generate_customer_kpi(df, OUTPUT_DIR)
    print_summary(df)

    logger.info("Generación de KPIs completada exitosamente.")


# ----------------------------------------------------------
# Ejecución directa
# ----------------------------------------------------------
if __name__ == "__main__":
    run_kpi()
