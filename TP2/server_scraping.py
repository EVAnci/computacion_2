import asyncio
import aiohttp
from aiohttp import web
import logging
from datetime import datetime
import argparse # Añadido para el setup

# --- Configuración de Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

async def fetch_url(session, url):
    """
    Esta función contiene la lógica pura de scraping para UNA url.
    Es la evolución de tu 'handle_scraping'.
    """
    log.info(f"Iniciando scraping de: {url}")
    try:
        # Usamos un timeout global para la petición
        timeout = aiohttp.ClientTimeout(total=30) 
        async with session.get(url, timeout=timeout) as response:
            
            # response.raise_for_status() es mejor que chequear 200
            # Lanzará una excepción si el status es 4xx o 5xx
            response.raise_for_status()
            
            content = await response.text() # Usar .text() para HTML, .read() para binario
            log.info(f'{url} content length: {len(content)}')

            # --- Aquí iría el parsing con BeautifulSoup (Funciones 1 y 2) ---
            # scraping_data = await parse_html(content) 
            
            # --- Aquí iría la llamada al Servidor B (Parte B) ---
            # processing_data = await request_processing(url)

            # Mockup temporal (como tenías)
            scraping_data = {"title": "Título de Ejemplo", "links": 10}
            processing_data = {"screenshot": "base64..."}
            
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


async def handle_scrape_request(request):
    """
    Este es el MANEJADOR DE RUTA (Handler).
    aiohttp crea una tarea para esta función CADA VEZ que
    un cliente hace un POST a /scrape.
    """
    try:
        # 1. Esperar input del cliente (NO es bloqueante)
        data = await request.json()
        url = data.get("url")

        if not url:
            return web.json_response(
                {"status": "error", "message": "Missing parameter: 'url'"},
                status=400
            )
        
        log.info(f"Petición recibida de {request.remote} para: {url}")

        # 2. Obtener la sesión compartida (ver init_app)
        session = request.app['client_session']

        # 3. Ejecutar la lógica de scraping
        scraped_content = await fetch_url(session, url)

        # 4. Devolver la respuesta
        status_code = 500 if scraped_content.get("status") == "error" else 200
        return web.json_response(scraped_content, status=status_code)

    except Exception as e:
        log.error(f"Error en el manejador principal: {e}", exc_info=True)
        return web.json_response(
            {"status": "error", "message": f"Error interno del servidor: {str(e)}"},
            status=500
        )

# --- Funciones de Arranque y Limpieza ---

async def on_startup(app):
    """Se ejecuta una vez, cuando el servidor arranca."""
    # Crea UNA sesión de cliente para que la use TODA la aplicación
    # Esto es mucho más eficiente (reúsa conexiones)
    app['client_session'] = aiohttp.ClientSession()
    log.info("Servidor arrancado, sesión de cliente creada.")

async def on_cleanup(app):
    """Se ejecuta una vez, cuando el servidor se apaga."""
    await app['client_session'].close()
    log.info("Cerrando sesión de cliente...")


def init_app():
    """Inicializa la aplicación web aiohttp."""
    app = web.Application()
    
    # 1. Definir rutas
    # Cualquier petición POST a http://.../scrape será manejada
    # por la función handle_scrape_request
    app.router.add_post("/scrape", handle_scrape_request)
    
    # 2. Registrar funciones de arranque/limpieza
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    
    return app


def main():
    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono")
    parser.add_argument('-i', '--ip', required=True, help="Dirección de escucha (soporta IPv4/IPv6)")
    parser.add_argument('-p', '--port', type=int, required=True, help="Puerto de escucha")
    args = parser.parse_args()

    # Tu función server() se reemplaza por esto:
    app = init_app()
    
    log.info(f"Iniciando servidor en http://{args.ip}:{args.port}")
    
    # Esto inicia el servidor y el event loop
    # y se queda corriendo para siempre (hasta Ctrl+C)
    web.run_app(app, host=args.ip, port=args.port)


if __name__ == '__main__':
    main()
