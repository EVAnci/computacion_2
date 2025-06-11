import json
from time import sleep
from numpy import mean, std 
from random import randint
from os import getpid

class Analizador:
    def __init__(self, tipo: str, canal_entrada, queue_salida):
        # tipo = "frecuencia", "presion", "oxigeno"
        self.__tipo__ = tipo
        # canal_entrada = Pipe o FIFO
        self.__canal_entrada__ = canal_entrada
        # queue_salida = multiprocessing.Queue()
        self.__queue_salida__ = queue_salida
        # lista con los últimos 30 valores
        self.__ventana__ = []
    
    def leer_datos(self):
        '''
        Lee los datos a través de el canal de entrada y los almacena en la ventana.
        '''
        # leemos el dato {"timestamp": "2025-06-11T15:32:09", "frecuencia": 122, "presion": [166, 99], "oxigeno": 100}
        self.__ventana__.append(json.loads(self.__canal_entrada__.recv())) # Pasar de string a json (falta validar datos entrantes)

    def procesar(self, n):
        '''
        Procesa los datos de la ventana.

        Retorno (str): {
            "tipo": "frecuencia", "presion" o "oxigeno"
            "timestamp": ...,
            "media": ...,
            "desv": ...
        }
        '''
        for _ in range(n):
            self.leer_datos()
            timestamp = self.__ventana__[-1].get('timestamp')

            # Obtiene los datos según el self.__tipo__ entonces:
            # Frecuen: datos = [55,59,65,70,90,...] todas las frecuencias cardiacas que hay en ventana 
            # Presión: datos = [[110,80], [112,90], ...] todas las listas de presion que hay en ventana
            # Oxigeno: datos = [92,95,96,95,96,...] todos los oxigenos que hay en ventana
            datos = [dato.get(self.__tipo__) for dato in self.__ventana__]
        
            # Se calculan las medias y desviacion según el self.__tipo__ entonces:
            # Frecuen: media = mean(datos) se devuelve la media datos, donde datos es la lista de frecuencias cardiacas de ventana
            # Presión: media = (mean(datos sistólicos), mean(datos diastólicos)) se devuelve una tupla con las medias (sistólica, diastólica)
            #          donde: 
            #               - `datos sistólicos` son, para cada dato de la lista de datos, el primer elemento (dato[0] for dato in datos)
            #               - `datos diastólicos` son, para cada dato de la lista de datos, el segundo elemento (dato[1] for dato in datos)
            # Oxigeno: media = mean(datos) al igual que frecuencia
            # Para la desviación estándar es lo mismo
            media = float(mean(datos)) if self.__tipo__ != 'presion' else [float(mean([dato[0] for dato in datos])), float(mean([dato[1] for dato in datos]))]
            desv = float(std(datos)) if self.__tipo__ != 'presion' else [float(std([dato[0] for dato in datos])), float(std([dato[1] for dato in datos]))]
            # Simula un calculo costoso (1 a 5 segundos float)
            sleep(randint(1,500)/100)

            resultado = {
                'tipo': self.__tipo__,
                'timestamp': timestamp,
                'media': media,
                'desv': desv
            }
            print(f'[{getpid()}] Procesado - {self.__tipo__} \t->\t{resultado}')
            self.__queue_salida__.put(json.dumps(resultado))