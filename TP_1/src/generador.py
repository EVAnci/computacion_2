from datetime import datetime
import random, json, time
from os import getpid

def generar_dato():
    '''
    Genera un diccionario por segundo:
    {
       "timestamp": "YYYY-MM-DDTHH:MM:SS",
       "frecuencia": int(60-180),
       "presion": [int(110-180), int(70-110)],
       "oxigeno": int(90-100)
    }
    '''
    # Devuelve un diccionario con los campos frecuencia, presión y oxígeno
    # {"timestamp": "2025-06-11T15:32:09", "frecuencia": 122, "presion": [166, 99], "oxigeno": 100}
    return json.dumps({
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "frecuencia": random.randint(60, 180),
        "presion": [random.randint(110, 180), random.randint(70, 110)], # [sistolica, diastolica]
        "oxigeno": random.randint(90, 100)
    })

def generar(n,pipe_frec,pipe_press,pipe_ox):
    for _ in range(n):
        dato = generar_dato()
        pipe_frec.send(dato)
        pipe_press.send(dato)
        pipe_ox.send(dato)
        print(f'[{getpid()}] Proceso generador escribiendo en pipes: {dato}')
        time.sleep(1)