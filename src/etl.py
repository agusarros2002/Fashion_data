"""
==========================================================
Fashion Data - ETL Pipeline
Autor/a: Agustina Arrospide
Versión: 1.3 (Centralizado con config.py + PEP 8)
Fecha: 01-11-2025
----------------------------------------------------------
Descripción:
    Ejecuta el proceso ETL para el dataset de ventas
    de moda (Fashion Retail Sales).

Incluye:
    - Limpieza de duplicados y nulos
    - Normalización de texto y fechas
    - Creación de variables derivadas
    - Exportación del dataset limpio para análisis y BI
==========================================================
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from src.config import RAW_DIR, PROCESSED_DIR, LOGS_ETL


# ----------------------------------------------------------
# Configuración general
# ----------------------------------------------------------
RAW_FILE = RAW_DIR / "Fashion_Retail_Sales.csv"
OUTPUT_FILE = PROCESSED_DIR / "fashion_sales_clean.csv"
LOG_FILE = LOGS_ETL / "etl_log.txt"



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ],
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# Funciones principales
# ----------------------------------------------------------
def load_data(path: Path) -> pd.DataFrame:
    """Carga el dataset original desde CSV."""
    logger.info("Cargando dataset desde: %s", path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    df = pd.read_csv(path)
    logger.info("Dataset cargado correctamente: %d filas, %d columnas", *df.shape)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza y normalización de datos crudos."""
    logger.info("Iniciando limpieza básica de datos...")

    # Normalizar nombres de columnas
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    # Eliminar duplicados
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates()
    logger.info("Duplicados eliminados: %d", dup_count)

    # Imputar valores nulos
    if "purchase_amount_usd" in df.columns:
        df["purchase_amount_usd"].fillna(df["purchase_amount_usd"].median(), inplace=True)
    if "review_rating" in df.columns:
        df["review_rating"].fillna(df["review_rating"].median(), inplace=True)

    # Normalizar texto
    for col in ["item_purchased", "payment_method"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title().str.strip()

    # Convertir fechas
    if "date_purchase" in df.columns:
        df["date_purchase"] = pd.to_datetime(
            df["date_purchase"], format="%d-%m-%Y", errors="coerce"
        )

    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Crea variables derivadas para análisis."""
    logger.info("Creando variables derivadas...")

    if "date_purchase" in df.columns:
        df["purchase_year"] = df["date_purchase"].dt.year
        df["purchase_month"] = df["date_purchase"].dt.month_name()
        df["purchase_day"] = df["date_purchase"].dt.day
        df["purchase_weekday"] = df["date_purchase"].dt.day_name()

    # Segmentación de ticket
    if "purchase_amount_usd" in df.columns:
        bins = [0, 100, 500, 1000, 5000]
        labels = ["Bajo", "Medio", "Alto", "Premium"]
        df["ticket_segment"] = pd.cut(
            df["purchase_amount_usd"], bins=bins, labels=labels, include_lowest=True
        )

    # Nivel de satisfacción
    if "review_rating" in df.columns:
        df["satisfaction_level"] = pd.cut(
            df["review_rating"],
            bins=[0, 2, 3.5, 5],
            labels=["Baja", "Media", "Alta"],
            include_lowest=True,
        )

    return df


def quality_report(df: pd.DataFrame) -> None:
    """Genera un resumen de calidad del dataset."""
    logger.info("Generando resumen de calidad...")
    nulos = df.isnull().sum()
    tipos = df.dtypes

    if nulos.any():
        logger.info("Columnas con nulos:\n%s", nulos[nulos > 0])
    logger.info("Tipos de datos:\n%s", tipos)
    logger.info("Dimensiones finales: %s", df.shape)


def save_clean_data(df: pd.DataFrame, path: Path) -> None:
    """Guarda el dataset procesado."""
    df.to_csv(path, index=False)
    logger.info("Archivo limpio guardado en: %s", path)


# ----------------------------------------------------------
# Función principal del pipeline
# ----------------------------------------------------------
def run_etl() -> None:
    """Ejecuta el pipeline ETL completo."""
    logger.info("Iniciando proceso ETL - Fashion Retail Sales")
    df_raw = load_data(RAW_FILE)
    df_clean = clean_data(df_raw)
    df_final = feature_engineering(df_clean)
    quality_report(df_final)
    save_clean_data(df_final, OUTPUT_FILE)
    logger.info("ETL finalizado correctamente.")


# ----------------------------------------------------------
# Ejecución directa
# ----------------------------------------------------------
if __name__ == "__main__":
    run_etl()
