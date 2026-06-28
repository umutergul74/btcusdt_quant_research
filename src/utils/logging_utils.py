import os
import logging
from datetime import datetime

def setup_logger(name: str, project_root: str = "/content/drive/MyDrive/btcusdt_quant_research") -> logging.Logger:
    """Sets up a logger that outputs to both console and a file in the logs directory."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_dir = os.path.join(project_root, "logs")
    if not os.path.exists(log_dir):
        # Fallback to local workspace
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)

    log_filename = f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    try:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to create log file at {log_path}: {e}")

    return logger
