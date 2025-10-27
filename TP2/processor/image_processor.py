import io
import base64
import logging
import requests # Para descargar las imágenes
from PIL import Image # Para procesarlas
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

log = logging.getLogger(__name__)

def generate_thumbnail(driver: WebDriver, max_thumbnails=5, size=(100, 100)):
    """
    Encuentra imágenes en la página, las descarga y crea thumbnails.
    Utiliza un driver de Selenium existente.
    """
    log.info(f"Iniciando procesamiento de imágenes...")
    thumbnails = []
    
    try:
        # 1. Encontrar todos los elementos <img>
        image_elements = driver.find_elements(By.TAG_NAME, "img")
        
        # 2. Obtener sus URLs (src)
        image_urls = []
        for img in image_elements:
            src = img.get_attribute('src')
            # Filtramos URLs válidas que podamos descargar
            if src and src.startswith('http'):
                image_urls.append(src)
                
        log.info(f"Se encontraron {len(image_urls)} imágenes. Procesando las primeras {max_thumbnails}...")

        # 3. Descargar y procesar las primeras 'max_thumbnails'
        for url in image_urls[:max_thumbnails]:
            try:
                # 4. Descargar la imagen
                # Usamos un timeout corto para no atascarnos en una imagen pesada
                response = requests.get(url, timeout=5)
                response.raise_for_status() # Lanza error si es 4xx/5xx

                # 5. Procesar en memoria con Pillow (PIL)
                img_data = io.BytesIO(response.content)
                with Image.open(img_data) as img:
                    # 'thumbnail' mantiene el aspect ratio, escalando
                    # a lo más grande que quepa en 'size'
                    img.thumbnail(size)
                    
                    # 6. Guardar el thumbnail en memoria
                    thumb_io = io.BytesIO()
                    # Convertimos a PNG para consistencia (GIFs pueden dar problemas)
                    img.save(thumb_io, format="PNG") 
                
                # 7. Codificar en Base64
                thumb_b64 = base64.b64encode(thumb_io.getvalue()).decode('utf-8')
                thumbnails.append(thumb_b64)
                
            except Exception as e:
                # Si una imagen falla, solo lo logueamos y continuamos
                log.warning(f"No se pudo procesar la imagen {url}: {e}")

        log.info(f"Se generaron {len(thumbnails)} thumbnails.")
        return thumbnails

    except Exception as e:
        log.error(f"Error al procesar imágenes: {e}")
        raise # Dejamos que el orquestador maneje el error
