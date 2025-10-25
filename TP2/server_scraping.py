import asyncio
import aiohttp

# This function handles the scraping requests asyncronically
async def handle_scraping(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.read()
            print(f'{url} content lenght: {len(content)}')
        else:
            print('Error al acceder')

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
