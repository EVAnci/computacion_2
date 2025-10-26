import asyncio
import aiohttp
from aiohttp import web
import logging
from datetime import datetime
import socket

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

    log.info(f"Scraping request received: {url}")

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
        log.warning(f"Timeout error: {url}")
        return web.json_response(
            {"status": "error", "message": "Timeout during the processing."},
            status=504
        )
    except Exception as e:
        log.error(f"Error processing {url}: {e}", exc_info=True)
        return web.json_response(
            {"status": "error", "message": str(e)},
            status=500
        )


# This function creates a server to handle connections.
# The server must use http protocol. Here urls are
# given by connected clients, and calls handle_scraping
# Should support ipv4 and ipv6 protocols
async def server():
    host6,port = '::',9401

    test_url = (
            'https://asherwycoff.com/',
            'https://holeinmyheart.neocities.org/',
            'https://www.librarian.net/',
            'https://hackernewsletter.com/',
            'https://dayzerosec.com/',
            'http://cow.net/cows/'
            )

    # As always interacting with low level sockets may be weird. So, what
    # we have here is some OS level constans (upper case). They are: 
    #   - AF_INET6 tells that the layer 3 protocol will be IPv6
    #   - SOCK_STREAM tells that layer 4 protocol will be TCP
    # After the creation of the socket, we set some aditional options 
    #   - SOL_SOCKET tells to use setsockopt() or getsockopt() os level functions
    #     that is because we want to tell that the socket can be reused when
    #     is on some of the following states: TIME_WAIT.
    #   - SO_REUSEARRD is the option we want to set in the socket. As simple as 
    #     that

    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            # Try to enable IPv4 mapping if is supported by the OS.
            srv.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            log.info('[+] Dual-stack enabled.')
        except OSError as e:
            log.error(f'[!] Dual-stack disabled: {e}')

        srv.bind((host6,port))

    # A producer-consumer problem, where clients produce requests 
    # and the sraper handler is the consumer.
    # Because clients must write requests somewere (a queue in 
    # this case), and waiting a user to write is a very slow IO 
    # task, green threads are a great solution.
    request_queue = asyncio.Queue(maxsize=5)

    async with aiohttp.ClientSession() as session:
        srv.listen(16)
        tasks = [handle_scraping(session,url) for url in test_url]
        await asyncio.gather(*tasks)

# This function manage the starting point, where the cli 
# and initialization parameters are given (like ip and port)
def main():
    asyncio.run(server())

if __name__ == '__main__':
    main()
