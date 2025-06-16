import json
from os import getpid
from src.blockchain import crear_bloque


def read_data(queue:any=None):
    """
    Reads and deserializes data from a queue.

    Parameters
    ----------
    queue : any, optional
        Queue from which data is retrieved. Each item in the queue is 
        expected to be a serialized JSON string.

    Returns
    -------
    list
        A list containing deserialized JSON objects retrieved from the queue.
    """

    datos = []
    for _ in range(3):
        raw = queue.get()
        resultado = json.loads(raw)
        datos.append(resultado)
    return datos

def alertar(datos:list=[]):
    """
    Analiza los datos de las sensores y devuelve una alarma
    si se supera alguno de los limites de seguridad.

    Parameters
    ----------
    datos : list
        Lista de diccionarios representando los datos de los sensores.
        Cada diccionario debe tener al menos las claves 'tipo' y 'media'.
        'tipo' puede tener valores 'frecuencia', 'presion' o 'oxigeno'.
        'media' es el valor medio de la magnitud que se esta midiendo.

    Returns
    -------
    bool
        True si se debe emitir una alarma, False en caso contrario.
    """
    for dato in datos:
        temp = dato.get('tipo')
        if temp == 'frecuencia':
            frec = dato.get('media')
        elif temp == 'presion':
            pres = dato.get('media')
        else:
            ox = dato.get('media')
    if frec > 200:
        return True
    elif pres[0] > 200 or pres[1] < 50:
        return True
    elif ox <= 90 or ox >= 100:
        return True
    return False


def verificar(queue:any=None, cantidad_total:int=0, verbose:bool=False):
    '''
    Lee resultados de la Queue, los valida y los muestra.

    Parameters
    ----------
    queue : multiprocessing.Queue
        Cola donde los analizadores escriben sus resultados.
    cantidad_total : int
        Cantidad total de mensajes esperados (n * número de analizadores).
    '''
    print(f'[{getpid()}] Verificador iniciado')
    blockchain = []
    prev_hash = "0" * 64  # Hash inicial para el primer bloque
    
    for _ in range(cantidad_total):
        datos = read_data(queue)
        alert = alertar(datos)
        bloque = crear_bloque(datos,alert,prev_hash)
        blockchain.append(bloque)
        prev_hash = bloque.get('hash')  # Encadenar hashes
        
        with open("blockchain.json", "w") as f:
            json.dump(blockchain, f, indent=4)
        
        if verbose:
            print(f"[{getpid()}] Verificado: {'Alerta' if alert else 'OK'} -> {datos}")
            print(bloque)

