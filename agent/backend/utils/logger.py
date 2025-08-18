import logging
import sys
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with formatting"""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Set level and add handler
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.propagate = False
    
    return logger
