"""
==========================================================
Fashion Data - Listado de Archivos
Autor/a: Agustina Arrospide
Versión: 1.3 (PEP 8 + Logging + config.py)
Fecha: 01-11-2025
----------------------------------------------------------
Genera un resumen de archivos dentro del proyecto.
Útil para auditorías o verificar estructura de carpetas.
==========================================================
"""

import logging
from pathlib import Path
from datetime import datetime
from src.config import BASE_DIR

# ----------------------------------------------------------
# Configuración general
# ----------------------------------------------------------
LOG_FILE = BASE_DIR / "data" / "processed" / "listado_archivos_log.txt"
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
# Función principal
# ----------------------------------------------------------
def list_files(base_dir: Path = BASE_DIR) -> None:
    """Lista recursivamente los archivos dentro de base_dir."""
    logger.info("Analizando estructura de: %s", base_dir)
    logger.info("=" * 80)

    for path in sorted(base_dir.rglob("*")):
        if path.is_file():
            size_kb = path.stat().st_size / 1024
            mod_time = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            logger.info("%s | %8.1f KB | Modif: %s", path, size_kb, mod_time)

    logger.info("Listado completo generado correctamente en %s", LOG_FILE)


if __name__ == "__main__":
    list_files()
