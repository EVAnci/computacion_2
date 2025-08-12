from multiprocessing import Lock
import multiprocessing
import time
import os

def worker(num, lock):
    """Función que simula una tarea pesada."""
    with lock:
        print(f"[Proceso {num}] PID: {os.getpid()} - Iniciando tarea")
        time.sleep(2)  # Simula trabajo
        print(f"[Proceso {num}] PID: {os.getpid()} - Tarea completada")

if __name__ == "__main__":
    procesos = []
    lock = Lock()
    # Crear 4 procesos
    for i in range(4):
        p = multiprocessing.Process(target=worker, args=(i,lock))
        procesos.append(p)
        p.start()  # Iniciar proceso

    for p in procesos:
        p.join()  # Esperar a que todos los procesos terminen

    print("Todos los procesos han finalizado.")
