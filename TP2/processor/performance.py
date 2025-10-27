import json
import logging
from selenium.webdriver.remote.webdriver import WebDriver

log = logging.getLogger(__name__)

def analyze_performance(url:str,driver: WebDriver):
    """
    Analiza el rendimiento usando un driver existente
    """
    log.info(f"Analizando rendimiento de {url}...")
    
    try:
        performance = json.loads(
            driver.execute_script("return JSON.stringify(window.performance.timing)")
        )
        resources = json.loads(
            driver.execute_script("return JSON.stringify(window.performance.getEntriesByType('resource'))")
        )

        load_time_ms = performance['loadEventEnd'] - performance['navigationStart']
        num_requests = len(resources)
        total_size_kb = sum(r.get('transferSize', 0) for r in resources) / 1024

        return {
            "load_time_ms": load_time_ms,
            "total_size_kb": round(total_size_kb, 2),
            "num_requests": num_requests
        }
    except Exception as e:
        log.error(f'Error al analizar rendimiento: {e}')
        raise
