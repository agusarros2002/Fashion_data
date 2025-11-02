"""
==========================================================
Fashion Data - Machine Learning (Regresión y Clasificación)
Autor/a: Agustina Arrospide
Versión: 1.6 (Fix OneHotEncoder TypeError + Persistencia)
Fecha: 02-11-2025
----------------------------------------------------------
Entrena modelos de regresión y clasificación sobre el
dataset procesado (fact_sales.csv) y guarda los modelos
entrenados en /models para su reutilización posterior.
==========================================================
"""

import argparse
import logging
import warnings
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    precision_recall_fscore_support,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

from src.config import PROCESSED_DIR, MODELS_DIR, LOGS_ML

# ----------------------------------------------------------
# Configuración general
# ----------------------------------------------------------
warnings.filterwarnings("ignore")
logging.getLogger("lightgbm").setLevel(logging.ERROR)

RANDOM_STATE = 42
INPUT_PATH = PROCESSED_DIR / "fashion_sales_clean.csv"

OUTPUT_DIR = PROCESSED_DIR / "ml"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_ML / "ml_log.txt"

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
# Compatibilidad opcional con XGBoost / LightGBM
# ----------------------------------------------------------
HAS_XGB, HAS_LGBM = False, False
try:
    import xgboost as xgb
    HAS_XGB = True
except Exception:
    pass

try:
    import lightgbm as lgb
    HAS_LGBM = True
except Exception:
    pass


def load_dataset() -> pd.DataFrame:
    """Carga el dataset procesado para modelado ML."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"No se encuentra {INPUT_PATH}. Ejecuta primero el ETL.")

    df = pd.read_csv(INPUT_PATH, parse_dates=["date_purchase"])
    df["year"] = df["date_purchase"].dt.year
    df["month"] = df["date_purchase"].dt.month

    bins = [0, 100, 500, 1000, np.inf]
    labels = ["Bajo", "Medio", "Alto", "Premium"]
    df["ticket_segment"] = pd.cut(df["purchase_amount_usd"], bins=bins, labels=labels)

    for col in ["item_purchased", "payment_method"]:
        top = df[col].value_counts().nlargest(20).index
        df[col] = df[col].where(df[col].isin(top), "OTHER")

    logger.info("Dataset cargado: %d filas, %d columnas", *df.shape)
    return df


def run_model(task: str = "both") -> None:
    """Ejecuta modelos ML según la tarea seleccionada."""
    logger.info("Iniciando modelado ML (task=%s)", task)
    df = load_dataset()

    # --- REGRESIÓN ---
    if task in ("both", "regression"):
        logger.info("Ejecutando regresión...")
        target = "review_rating"
        num = ["purchase_amount_usd", "year", "month"]
        cat = ["payment_method", "item_purchased"]

        df = df.dropna(subset=[target])
        X, y = df[num + cat], df[target].astype(float)

        # ✅ FIX: asegurar tipos homogéneos
        X[cat] = X[cat].astype(str)

        preproc = ColumnTransformer([
            ("num", StandardScaler(), num),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
        ])

        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)

        models = {
            "linear_regression": LinearRegression(),
            "random_forest_regression": RandomForestRegressor(
                n_estimators=400, random_state=RANDOM_STATE, n_jobs=-1),
        }

        results = []
        for name, model in models.items():
            pipe = Pipeline([("prep", preproc), ("model", model)])
            pipe.fit(Xtr, ytr)
            preds = pipe.predict(Xte)
            results.append({
                "model": name,
                "MAE": mean_absolute_error(yte, preds),
                "RMSE": np.sqrt(mean_squared_error(yte, preds)),
                "R2": r2_score(yte, preds),
            })
            dump(pipe, MODELS_DIR / f"{name}.pkl")
            logger.info("Modelo %s guardado correctamente.", name)

        pd.DataFrame(results).to_csv(OUTPUT_DIR / "ml_results_regression.csv", index=False)
        logger.info("Resultados de regresión guardados correctamente.")

    # --- CLASIFICACIÓN ---
    if task in ("both", "classification"):
        logger.info("Ejecutando clasificación...")
        target = "ticket_segment"
        num = ["review_rating", "year", "month"]
        cat = ["payment_method", "item_purchased"]

        df = df.dropna(subset=[target])
        X, y_str = df[num + cat], df[target].astype(str)
        le = LabelEncoder()
        y = le.fit_transform(y_str)

        # ✅ FIX: asegurar tipos homogéneos
        X[cat] = X[cat].astype(str)

        preproc = ColumnTransformer([
            ("num", StandardScaler(), num),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
        ])

        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)

        models = {
            "logistic_regression": LogisticRegression(max_iter=200),
            "random_forest_classification": RandomForestClassifier(
                n_estimators=500, random_state=RANDOM_STATE, n_jobs=-1),
        }

        results = []
        for name, model in models.items():
            pipe = Pipeline([("prep", preproc), ("model", model)])
            pipe.fit(Xtr, ytr)
            preds = pipe.predict(Xte)
            pr, rc, f1, _ = precision_recall_fscore_support(yte, preds, average="macro")
            results.append({
                "model": name,
                "accuracy": accuracy_score(yte, preds),
                "precision_macro": pr,
                "recall_macro": rc,
                "f1_macro": f1,
            })
            dump(pipe, MODELS_DIR / f"{name}.pkl")
            logger.info("Modelo %s guardado correctamente.", name)

        pd.DataFrame(results).to_csv(OUTPUT_DIR / "ml_results_classification.csv", index=False)
        logger.info("Resultados de clasificación guardados correctamente.")

        cm = confusion_matrix(yte, preds)
        pd.DataFrame(cm, index=le.classes_, columns=le.classes_).to_csv(
            OUTPUT_DIR / "confusion_matrix_ticket_segment.csv", index=False
        )
        logger.info("Matriz de confusión guardada correctamente.")

    logger.info("Modelado ML completado correctamente.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        type=str,
        default="both",
        choices=["both", "regression", "classification"],
        help="Tarea a ejecutar: both | regression | classification",
    )
    args = parser.parse_args()
    run_model(task=args.task)