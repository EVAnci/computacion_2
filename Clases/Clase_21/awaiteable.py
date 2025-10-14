import asyncio

async def mi_corrutina():
    return 42

# Esto es un awaitable (es una corrutina)
resultado = await mi_corrutina()  # ✓ Funciona

# Esto NO es awaitable
import time
await time.sleep(1)  # ✗ TypeError: object float can't be used in 'await' expression
