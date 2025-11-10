import asyncio
import aiohttp
import json
import argparse
import sys       # Para stderr
import os        # para crear directorios
import base64    # para decodificar imágenes
from pathlib import Path # para manejar rutas de archivos de forma cómoda
from urllib.parse import urlparse

def clean_url_for_path(url: str) -> str:
    """
    Convierte una URL (ej: 'https://www.google.com/path')
    en un nombre de directorio seguro (ej: 'www.google.com').
    """
    try:
        # Si la URL no tiene esquema, urlparse necesita ayuda
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
            
        parsed_url = urlparse(url)
        # 'netloc' es la parte 'www.google.com'
        domain = parsed_url.netloc or "url_desconocida"
        
        # Elimina 'www.' si existe, para nombres más cortos
        if domain.startswith("www."):
            domain = domain[4:]
            
        return domain
    except Exception:
        return "url_invalida"
    
def save_decoded_image(file_path: Path, base64_data: str):
    """Decodifica una cadena Base64 y la guarda como un archivo de imagen."""
    try:
        # Asegura que el directorio padre exista
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        image_data = base64.b64decode(base64_data)
        
        with open(file_path, 'wb') as f: # 'wb' = write binary
            f.write(image_data)
        print(f"Imagen guardada: {file_path}")
            
    except Exception as e:
        print(f"Error: Archivo {file_path}. {e}", file=sys.stderr)

async def scrape_and_save(session: aiohttp.ClientSession, endpoint: str, url: str):
    print(f"-> Iniciando scrape para: {url}")
    try:
        async with session.post(endpoint, json={"url": url}, timeout=60) as r:
            print("Respuesta HTTP:", r.status)
            r.raise_for_status()  # Lanza una excepción para errores HTTP (4xx, 5xx)
            
            data = await r.json()
            
            # Imprime los primeros 2000 caracteres del JSON formateado
            print(f"\n[+]  scrape parcial de {url}:")
            print(json.dumps(data, indent=2)[:2000])
            print("... [truncado]\n")

            # --- INICIO DE LÓGICA DE GUARDADO ---
            
            # 1. Crear rutas
            base_dir_name = clean_url_for_path(url)
            page_dir = Path("pages") / base_dir_name
            media_dir = page_dir / "media"
            
            # 2. Guardar el JSON principal
            page_dir.mkdir(parents=True, exist_ok=True)
            json_path = page_dir / "page_analysis.json"
            
            try:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print(f"\nAnálisis JSON guardado en: {json_path}")
            except IOError as e:
                print(f"Error al guardar JSON: {e}", file=sys.stderr)
            
            
            # 3. Guardar imágenes y miniaturas
            processing_data = data.get("processing_data", {})
            
            # Guardar Screenshot
            screenshot_b64 = processing_data.get("screenshot")
            if screenshot_b64:
                screenshot_path = media_dir / "screenshot.png"
                save_decoded_image(screenshot_path, screenshot_b64)
            
            # Guardar Miniaturas (Thumbnails)
            thumbnails_b64 = processing_data.get("thumbnails", [])
            if not thumbnails_b64:
                print("No se encontraron miniaturas (thumbnails) en la respuesta.")
            
            for i, thumb_b64 in enumerate(thumbnails_b64):
                if thumb_b64:
                    thumb_path = media_dir / f"thumbnail_{i+1}.png"
                    save_decoded_image(thumb_path, thumb_b64)
                    
            print(f"\nResultados guardados en el directorio: {page_dir.absolute()}")
            # --- FIN DE LÓGICA DE GUARDADO ---

    except aiohttp.ClientConnectorError:
        print(f"\nError: No se pudo conectar a {endpoint}", file=sys.stderr)
        print("¿Estás seguro de que el Servidor A está corriendo en esa dirección?", file=sys.stderr)
    except aiohttp.ClientResponseError as e:
        print(f"\nError del servidor: HTTP {e}", file=sys.stderr)
    except asyncio.TimeoutError:
        print(f"\nError: Timeout. El servidor tardó más de 60s en responder.", file=sys.stderr)
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}", file=sys.stderr)

async def main(args):
    """
    Función principal asíncrona que contacta al servidor.
    Recibe los argumentos parseados.
    """
    urls = args.urls
    host = args.host
    port = args.port

    # Añadimos los corchetes al host si es una dirección IPv6
    # para que la URL sea válida (ej: http://[::1]:8080)
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
            
    endpoint = f"http://{host}:{port}/scrape"
    
    print(f"Contactando {endpoint} para scrapear: {len(urls)} URL(s)")

    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(scrape_and_save(session, endpoint, url))
        results = await asyncio.gather(*tasks)



if __name__ == "__main__":
    TEST_URLS = (
        'https://asherwycoff.com/',
        'https://holeinmyheart.neocities.org/',
        'https://www.librarian.net/',
        'https://hackernewsletter.com/',
        'https://dayzerosec.com/',
        'http://cow.net/cows/',
        'https://google.com',
        'https://wikipedia.org',
        'https://python.org',
        'https://duckduckgo.com'
    )

    # 1. Configurar el parser
    parser = argparse.ArgumentParser(
        description="Cliente para el Servidor de Scraping Web",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Muestra los defaults en -h
    )
    
    # 2. Definir los argumentos
    
    # Argumento posicional (cero o más)
    parser.add_argument(
        "urls",
        nargs="*",
        help="La URL completa que se desea scrapear (ej: https://www.python.org)"
    )

    parser.add_argument(
        "-t", "--use_test_urls",
        action="store_true",
        help="Usar un conjunto de URLs de prueba predefinidas"
    )
    
    # Argumentos opcionales (con -)
    parser.add_argument(
        "-H", "--host",
        default="[::1]",
        help="Dirección IP o host del Servidor A"
    )
    
    parser.add_argument(
        "-P", "--port",
        type=int,
        default=8080,
        help="Puerto del Servidor A"
    )

    args = parser.parse_args()

    if args.use_test_urls:
        print(f"[+] Usando {len(TEST_URLS)} URLs de prueba predefinidas...")
        args.urls = TEST_URLS
    elif not args.urls:
        # Si no se usa el flag Y TAMPOCO se dieron URLs, es un error.
        parser.error("Debes proporcionar al menos una URL o usar la opción -t/--use-test-urls.")
        # parser.error() imprime el mensaje y sale del script
    
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nCliente detenido.")