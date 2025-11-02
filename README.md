# 👗 Fashion Data – Data Analytics & Machine Learning Pipeline

Proyecto integral de analítica y machine learning para ventas minoristas de moda.  
Incluye ETL, generación de KPIs, modelado predictivo, evaluación visual y dashboard automatizado.

Desarrollado por **Agustina Arrospide**  
GitHub: [@agusarros2002](https://github.com/agusarros2002)

---

## 📂 Estructura del proyecto

```
Fashion_Data/
├── data/
│   ├── raw/                 # Datos originales (Fashion_Retail_Sales.csv)
│   ├── processed/           # Datos limpios, KPIs, métricas, logs
│   ├── processed/ml         # Datos limpios, KPIs, métricas, logs
│   └── processed/kpi/       # KPIs por ventas, satisfacción, clientes
│
├── report/
│   └── figuras/
│       ├── etl/             # Figuras del proceso ETL
│       ├── kpi/             # Figuras de KPIs
│       ├── models/          # Resultados y comparativas de ML
│       ├── evaluacion/      # Visualizaciones de performance
│       └── shap/            # Explicabilidad de modelos
│
├── models/                  # Modelos entrenados serializados (.pkl)
│   ├── linear_regression.pkl
│   ├── logistic_regression.pkl
│   ├── random_forest_classification.pkl
│   └── random_forest_regression.pkl
│
├── src/
│   ├── app.py               # Orquestador principal del pipeline
│   ├── config.py            # Configuración global, rutas y save_figure()
│   ├── etl.py               # Limpieza, transformación y enriquecimiento
│   ├── kpi.py               # Cálculo de indicadores clave (KPIs)
│   ├── model.py             # Entrenamiento y guardado de modelos ML
│   ├── evaluation.py        # Gráficos y evaluación de resultados
│   └── dashboards.py        # Modelo estrella (LightGBM + SHAP)
│
├── notebooks/
│   └── 01_exploracion.ipynb # Análisis exploratorio (EDA)
│
├── powerbi/                 # carpeta exclusiva para Power BI
│   ├── fashion_data_dashboard.pbix
│   ├── Figura_4_1_Evolucion_mensual_ventas.png
│   ├── Figura_4_2_Distribucion_satisfaccion_segmento.png
├── .venv/                   # Entorno virtual Python
├── README.md
├── CHANGELOG.md
└── requirements.txt
```

---

## 🚀 Ejecución del pipeline completo

```bash
python -m src.app
```

El proceso ejecuta automáticamente:
```
ETL → KPI → MODEL → EVALUATION → DASHBOARD
```

---

## 🧠 Modelos entrenados

Durante la ejecución del módulo `src/model.py`, se entrenan y **guardan automáticamente** los siguientes modelos:

| Tipo | Modelo | Archivo |
|------|---------|----------|
| Regresión | LinearRegression | `models/linear_regression.pkl` |
| Regresión | RandomForestRegressor | `models/random_forest_regression.pkl` |
| Clasificación | LogisticRegression | `models/logistic_regression.pkl` |
| Clasificación | RandomForestClassifier | `models/random_forest_classification.pkl` |

> Los modelos se guardan con `joblib` para su reutilización o despliegue posterior.

---

## 🧾 Logs y resultados

- `data/processed/ml_results_regression.csv`
- `data/processed/ml_results_classification.csv`
- `data/processed/kpi/*.csv`
- `data/processed/dashboard_log.txt`
- `report/figuras/*` → Figuras automáticas por módulo

---

## ⚙️ Requisitos

Instala las dependencias dentro de tu entorno virtual:

```bash
pip install -r requirements.txt
```

---

## 📈 Dashboard principal

El módulo `src/dashboards.py` entrena un modelo LightGBM sobre las ventas procesadas,  
calcula importancia de variables con SHAP y genera un gráfico resumen automático.

Salida:
```
report/figuras/shap/fig_shap_summary.png
```

---

## 📚 Versionado
Consulta el archivo [`CHANGELOG.md`](CHANGELOG.md) para ver el historial de cambios y versiones.

---

## 🧑‍💻 Autor
**Agustina Arrospide**  
📍 Data Analytics & Machine Learning  
🔗 [GitHub – @agusarros2002](https://github.com/agusarros2002)
