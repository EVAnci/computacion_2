import multiprocessing
import os
import time

def worker():
    """Función que se ejecutará en un proceso hijo."""
    print(f"Proceso hijo: PID={os.getpid()}, PPID={os.getppid()}")
    time.sleep(2)  # Simula trabajo
    print(f"Proceso hijo {os.getpid()} finalizado.")

if __name__ == "__main__":
    print(f"Proceso principal: PID={os.getpid()}")

    # Crear un nuevo proceso
    proceso = multiprocessing.Process(target=worker)

    # Iniciar el proceso
    proceso.start()

    # Esperar a que el proceso hijo termine
    proceso.join()

    print("Proceso principal finalizado.")
