import json
from os import getpid

class Verificador:
    def __init__(self, queues_entrada):
        # queues_entrada: dict con claves "frecuencia", "presion", "oxigeno"
        ...

    def verificar_y_guardar():
        # Junta 3 resultados por timestamp, verifica, construye bloque, guarda en JSON
        ...

# src/verificador.py



def verificar(queue:any=None, cantidad_total:int=0):
    '''
    Lee resultados de la Queue, los valida y los muestra.

    Parameters
    ----------
    queue : multiprocessing.Queue
        Cola donde los analizadores escriben sus resultados.
    cantidad_total : int
        Cantidad total de mensajes esperados (n * número de analizadores).
    '''
    for _ in range(cantidad_total):
        raw = queue.get() # El verificador debe saber cuántas veces tiene que hacer queue.get() para leer todos los resultados.
                          #Si se hacen menos get() de los que hay en la cola se pierden resultados.
        resultado = json.loads(raw)
        tipo = resultado.get('tipo')
        timestamp = resultado.get('timestamp')
        media = resultado.get('media')
        desv = resultado.get('desv')

        print(f"[{getpid()}] Verificado OK -> {resultado}")                  

