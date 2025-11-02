"""
==========================================================
Fashion Data - Dashboard / Modelo Estrella (LightGBM + SHAP)
Versión: 1.5 (config.py + save_figure)
==========================================================
"""

import logging
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from src.config import PROCESSED_DIR, save_figure, FIGURES_SHAP, LOGS_DASH

LOG_FILE = LOGS_DASH / "dashboard_log.txt"
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] - %(message)s",
                    handlers=[logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)


def train_dashboard_model():
    df = pd.read_csv(PROCESSED_DIR / "fashion_sales_clean.csv")
    df["target"] = np.log1p(df["purchase_amount_usd"])
    df = df.dropna(subset=["target"])

    X = pd.get_dummies(df[["review_rating", "purchase_year", "purchase_month"]], drop_first=True)
    y = df["target"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    params = {"objective": "regression", "metric": "rmse", "learning_rate": 0.05}
    model = lgb.train(params, lgb.Dataset(X_train, label=y_train),
                      valid_sets=[lgb.Dataset(X_val, label=y_val)],
                      num_boost_round=500,
                      callbacks=[lgb.early_stopping(50)])

    preds = np.expm1(model.predict(X_val))
    y_val_real = np.expm1(y_val)
    rmse = np.sqrt(mean_squared_error(y_val_real, preds))
    r2 = r2_score(y_val_real, preds)
    logger.info("✅ RMSE=%.2f | R²=%.3f", rmse, r2)

    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_val)
        shap.summary_plot(shap_values, X_val, show=False)
        save_figure("shap", "fig_shap_summary.png")
    except Exception as e:
        logger.warning("SHAP no se pudo calcular: %s", e)


def run_dashboard():
    logger.info("Iniciando modelo estrella...")
    train_dashboard_model()
    logger.info("Dashboard completado correctamente.")


if __name__ == "__main__":
    run_dashboard()
