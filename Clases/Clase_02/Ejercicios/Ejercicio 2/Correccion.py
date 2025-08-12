import os
import time
from random import randint

def heavy_load_calculation():
    delay = randint(2, 6)  # Cada hijo tiene su propio número aleatorio
    time.sleep(delay)
    print(f'Soy un proceso hijo - PID: {os.getpid()}; PPID: {os.getppid()}. Terminé después de {delay} segundos.')

def create_processes(n):
    children = []
    for _ in range(n):
        pid = os.fork()
        if pid == 0:  # Proceso hijo
            heavy_load_calculation()
            os._exit(0)  # Termina correctamente el proceso hijo
        else:
            children.append(pid)  # Guarda el PID del hijo
    return children

def main():
    num_of_processes = int(input('Escriba un número entero indicando la cantidad de procesos a crear: '))

    children = create_processes(num_of_processes)

    print('Esperando a que todos los procesos creados terminen...')
    for child in children:
        os.waitpid(child, 0)  # Espera a cada hijo
    print('Todos los procesos han terminado, finalizando...')

if __name__ == '__main__':
    main()
