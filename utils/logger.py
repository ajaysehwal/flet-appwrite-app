# utils/logger.py
import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger():
    logger = logging.getLogger('flet_auth')
    logger.setLevel(logging.INFO)
    
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Create log file path
    log_file = log_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger