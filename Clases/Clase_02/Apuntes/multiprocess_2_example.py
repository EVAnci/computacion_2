import multiprocessing
import os
import time
from random import randint

def worker(numero, mensaje):
    """Cada proceso ejecutará esta función"""
    tiempo_espera = randint(1, 5)
    print(f"Proceso {numero}: PID={os.getpid()}, PPID={os.getppid()} - {mensaje} - Esperando {tiempo_espera} segundos...")
    time.sleep(tiempo_espera)
    print(f"Proceso {numero} (PID={os.getpid()}) ha terminado.")

if __name__ == "__main__":
    print(f"Proceso principal: PID={os.getpid()}")

    num_procesos = 4  # Número de procesos a crear
    procesos = []

    # Crear e iniciar procesos
    for i in range(num_procesos):
        proceso = multiprocessing.Process(target=worker, args=(i+1,"mensaje de prueba"))
        procesos.append(proceso)
        proceso.start()

    # Esperar a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()

    print("Todos los procesos han finalizado.")
