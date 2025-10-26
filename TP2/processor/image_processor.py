from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64
import logging

log = logging.getLogger(__name__)

def take_screenshot(url):
    """
    Toma un screenshot usando Selenium (¡operación CPU/I/O intensiva!)
    Esta función se ejecuta en un proceso separado.
    """
    log.info(f"Tomando screenshot de {url}...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20) # Timeout para la carga
        driver.get(url)
        
        # Espera un poco (no es ideal, pero simple)
        driver.implicitly_wait(2) 
        
        png_data = driver.get_screenshot_as_png()
        b64_data = base64.b64encode(png_data).decode('utf-8')
        log.info(f"Screenshot de {url} completado.")
        return b64_data
        
    except Exception as e:
        log.error(f"Error al tomar screenshot de {url}: {e}")
        raise
    finally:
        if driver:
            driver.quit()
