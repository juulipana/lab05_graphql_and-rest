import time
from typing import Dict, Any


def measure_response_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        return result, elapsed_ms
    return wrapper


def calculate_response_size(response_content: bytes) -> int:
    return len(response_content)


def create_metric_record(scenario: str, treatment: str, iteration: int, 
                         response_time_ms: float, response_size_bytes: int) -> Dict[str, Any]:
    return {
        'scenario': scenario,
        'treatment': treatment,
        'iteration': iteration,
        'response_time_ms': response_time_ms,
        'response_size_bytes': response_size_bytes
    }

