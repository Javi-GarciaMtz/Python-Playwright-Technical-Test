import logging
import sys
from pathlib import Path
from datetime import datetime

# ? Configuración básica
APP_NAME = "app"
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

def setup_logger():
    """Configura y devuelve el logger principal de la aplicación"""
    # ? Crear directorio de logs
    log_folder = Path("logs")
    log_folder.mkdir(exist_ok=True)
    
    # ? Nombre del archivo con fecha actual
    log_file = log_folder / f"app_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    # ? Configurar logger
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(LOG_LEVEL)
    
    # ? Evitar duplicación de handlers
    if logger.hasHandlers():
        return logger
        
    # ? Agregar handler de consola
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console)
    
    # ? Agregar handler de archivo
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    
    return logger

# ? Instancia global del logger
logger = setup_logger()