import logging
import sys
from datetime import datetime


def setup_logger(name: str = "experiment", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def log_experiment_start(logger: logging.Logger, scenario: str, treatment: str, iteration: int):
    logger.info(f"Iniciando execução - Cenário: {scenario}, Tratamento: {treatment}, Iteração: {iteration}")


def log_experiment_end(logger: logging.Logger, scenario: str, treatment: str, iteration: int, 
                       response_time_ms: float, response_size_bytes: int):
    logger.info(
        f"Concluída execução - Cenário: {scenario}, Tratamento: {treatment}, Iteração: {iteration}, "
        f"Tempo: {response_time_ms:.2f}ms, Tamanho: {response_size_bytes} bytes"
    )


def log_error(logger: logging.Logger, scenario: str, treatment: str, iteration: int, error: Exception):
    logger.error(
        f"Erro na execução - Cenário: {scenario}, Tratamento: {treatment}, Iteração: {iteration}, "
        f"Erro: {str(error)}"
    )

