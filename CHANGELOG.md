# 📘 CHANGELOG – Fashion Data

> Registro histórico de cambios, mejoras y versiones del proyecto.

---

## [1.5.0] – 2025-11-02
### ✨ Mejoras
- Integración total de rutas y utilidades desde `config.py`.
- Creación automática de estructura de carpetas (data, report, figures, models).
- Función `save_figure()` centralizada y mejorada.
- Pipeline modular y estable (`ETL → KPI → MODEL → EVALUATION → DASHBOARD`).

### 🐞 Correcciones
- Eliminado error `ModuleNotFoundError: No module named 'src'`.
- Solucionado bug de rutas duplicadas en figuras.
- Eliminados mensajes “Using categorical units…” al ordenar meses.

### 🧠 Refactor
- Código PEP8 + docstrings unificados.
- Logs consistentes y sin advertencias.
- Configuración de entorno virtual `.venv` aislado y limpio.

---

## [1.4.0] – 2025-10-28
### ✨ Mejoras
- KPI reorganizados y optimizados.
- Estructura de `src` estandarizada.
- Creación de funciones de resumen automático.

---

## [1.3.0] – 2025-10-26
### 🧩 Novedades
- Implementación del módulo `kpi.py`.
- Nuevo pipeline ETL con resumen de calidad y features derivados.
- Visualizaciones iniciales ETL (método de pago y montos).

---

## [1.2.0] – 2025-10-22
### 🧠 Exploración
- Notebook `01_exploracion.ipynb` como análisis exploratorio principal (EDA).
- Validación de dataset base y features iniciales.

---

## [1.0.0] – 2025-10-15
### 🚀 Primera versión
- Configuración inicial del entorno.
- Ingesta de dataset `Fashion_Retail_Sales.csv`.
- Limpieza básica y exportación de datos procesados.
