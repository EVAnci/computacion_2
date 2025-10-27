import aiohttp
import asyncio
import logging
from datetime import datetime

from scraper.html_parser import scrape_page_data
from common.protocol import request_processing_from_server_b

log = logging.getLogger(__name__)

async def fetch_url(session, url):
    """
    Esta función contiene la lógica pura de scraping para una url.
    Es la evolución de tu 'handle_scraping'.
    """
    log.info(f"Iniciando scraping de: {url}")
    try:
        # timeout global para la petición
        timeout = aiohttp.ClientTimeout(total=30) 
        async with session.get(url, timeout=timeout) as response:
            
            # Lanzará una excepción si el status es 4xx o 5xx
            response.raise_for_status()
            
            content = await response.text() # Como leemos html, es mejor usar text que read
            log.info(f'{url} content length: {len(content)}')

            # --- Parsing con BeautifulSoup ---
            scraping_data = await scrape_page_data(content)
            
            # --- Llamada al Servidor B ---
            # processing_data = await request_processing(url)
            task_data = {'url':url}
            processing_data = await request_processing_from_server_b(
                    server_b_config=('127.0.0.2','8000'),
                    task_data=task_data
                )

            # Mockup temporal 
            # processing_data = {"screenshot": "base64"}
            
            return {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "scraping_data": scraping_data,
                "processing_data": processing_data,
                "status": "success"
            }

    except asyncio.TimeoutError:
        log.warning(f"Timeout al procesar {url}")
        return {"status": "error", "message": "Timeout durante el scraping (30s)", "url": url}
    except aiohttp.ClientError as e:
        log.error(f"Error de cliente HTTP procesando {url}: {e}")
        return {"status": "error", "message": f"Error de HTTP: {e}", "url": url}
    except Exception as e:
        log.error(f"Error inesperado procesando {url}: {e}", exc_info=True)
        return {"status": "error", "message": f"Error inesperado: {str(e)}", "url": url}
