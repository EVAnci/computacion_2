class Bloque:
    def __init__(self, datos, timestamp, prev_hash):
        # Guarda y calcula hash del bloque
        ...

def guardar_bloque(bloque, archivo="blockchain.json"):
    # Append persistente
    ...

def cargar_cadena(archivo="blockchain.json"):
    # Devuelve la lista de bloques
    ...
