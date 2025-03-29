import os
import time

def create_child():
    pid = os.fork()
    if pid == 0:  # Proceso hijo
        time.sleep(2)
        print(f'Soy un proceso hijo - PID: {os.getpid()}, PPID: {os.getppid()}')
        os._exit(0)  # Finaliza el proceso hijo correctamente
    return pid  # Devuelve el PID del hijo

def main():
    children = [create_child() for _ in range(3)]

    print(f'Soy el proceso padre - PID: {os.getpid()}; esperando a los procesos hijos.')
    for child in children:
        os.waitpid(child, 0)  # Espera a cada hijo
    print('Todos los procesos han terminado. Saliendo...')

if __name__ == '__main__':
    main()
