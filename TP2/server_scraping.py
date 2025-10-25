import asyncio
import aiohttp
from aiohttp import web
import logging
from datetime import datetime

# Use logging is a better way to 'print' logs 
# while the server is running
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# This function handles the scraping requests asyncronically
async def handle_scraping(session, url):
    if not url:
        return web.json_response(
            {"status": "error", "message": "Missing parameter: 'url'"},
            status=400
        )

    log.info(f"Recibida solicitud de scraping para: {url}")

    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                log.info(f'{url} content lenght: {len(content)}')
            else:
                return response

        # To debug, mock scraping_data and processing_data
        scraping_data,processing_data='hello','world'
    
        scraped_content = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "scraping_data": scraping_data,
            "processing_data": processing_data,
            "status": "success"
        }

        return web.json_response(scraped_content, status=200)

    except asyncio.TimeoutError:
        log.warning(f"Timeout al procesar {url}")
        return web.json_response(
            {"status": "error", "message": "Timeout durante el procesamiento"},
            status=504
        )
    except Exception as e:
        log.error(f"Error procesando {url}: {e}", exc_info=True)
        return web.json_response(
            {"status": "error", "message": str(e)},
            status=500
        )


# This function creates a server to handle connections.
# The server must use http protocol. Here urls are
# given by connected clients, and calls handle_scraping
async def server():
    test_url = (
            'https://asherwycoff.com/',
            'https://holeinmyheart.neocities.org/',
            'https://www.librarian.net/',
            'https://hackernewsletter.com/',
            'https://dayzerosec.com/',
            'http://cow.net/cows/'
            )
    async with aiohttp.ClientSession() as session:
        tasks = [handle_scraping(session,url) for url in test_url]
        await asyncio.gather(*tasks)

# This function manage the starting point, where the cli 
# and initialization parameters are given (like ip and port)
def main():
    asyncio.run(server())

if __name__ == '__main__':
    main()
