import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from threading import Lock

appdata_dir = os.getenv("LOCALAPPDATA")
niv_louie_app_data = os.path.join(appdata_dir, "Niv_Louie")
os.makedirs(niv_louie_app_data, exist_ok=True)

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

		#Creates logs folder if it doesn't exist
        logs_folder = os.path.join(niv_louie_app_data,"logs")
        os.makedirs(logs_folder , exist_ok=True)
        # Create rotating file handler
        log_file_path = os.path.join(logs_folder , "niv_louie.log")
        fh = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)  # 5 MB per file, 5 backups
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger

class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls, name=__name__):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance.logger = get_logger(name)
        return cls._instance

    def info(self, message):
        try:
            self.logger.info(message)
        except Exception as e:
            print(f"Logging error: {e}")

    def debug(self, message):
        try:
            self.logger.debug(message)
        except Exception as e:
            print(f"Logging error: {e}")

    def error(self, message):
        try:
            self.logger.error(message)
        except Exception as e:
            print(f"Logging error: {e}")

    def warning(self, message):
        try:
            self.logger.warning(message)
        except Exception as e:
            print(f"Logging error: {e}")

    def critical(self, message):
        try:
            self.logger.critical(message)
        except Exception as e:
            print(f"Logging error: {e}")

# Create a logger instance
logger = Logger()
logger.info("Logger initialized")