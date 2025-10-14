import requests
import asyncio
import aiohttp

# async def descargar_async():
#     response = await requests.get('https://um.edu.ar')

async def descargar_async():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://example.com") as response:  # ✓ Correcto
            return await response.text()

asyncio.run(descargar_async())
print('hola')
