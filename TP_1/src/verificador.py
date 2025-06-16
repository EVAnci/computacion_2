import json
from os import getpid

def read_data(queue:any=None):
    datos = []
    for _ in range(3):
        raw = queue.get()
        resultado = json.loads(raw)
        datos.append(resultado)
    return datos

def alertar(datos:list=[]):
    for dato in datos:
        temp = dato.get('tipo')
        if temp == 'frecuencia':
            frec = dato.get('media')
        elif temp == 'presion':
            pres = dato.get('media')
        else:
            ox = dato.get('media')
    print(frec, pres, ox)
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
    for _ in range(cantidad_total):
        datos = read_data(queue)
        alert = alertar(datos)

        if verbose:
            print(f"[{getpid()}] Verificado: {'Alerta' if alert else 'OK'} -> {datos}")                  

