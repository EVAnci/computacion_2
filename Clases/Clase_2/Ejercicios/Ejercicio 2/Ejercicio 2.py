import os, time
from random import randint

def heavy_load_calculation(number):
    # Esta función simula una operación costosa temporalmente
    for _ in range(number):
        time.sleep(1)

def create_process(n, process_list):
    process_list.append(os.getpid())
    for i in range(n):
        if os.getpid() == process_list[0]:
            process_list.append(os.fork())
        else:
            return i
    return n if not(process_list[0]==os.getpid()) else 0

def main():
    num_of_process = int(input('Escriba un número entero indicando la cantidad de procesos que desea crear: '))
    
    # Creo un objeto lista para pasarlo como referencia a la función
    process_list = []
    process_number = create_process(num_of_process, process_list)

    if os.getpid() != process_list[0]:
        number = randint(2,6)
        heavy_load_calculation(number)
        print(f'Soy el proceso hijo {process_number} - PID: {os.getpid()}; PPID: {os.getppid()}; Espera mínima: {number}')
    else:
        print(f'Soy el proceso padre {process_number} - PID: {os.getpid()}')
        print('Esperando a que todos los procesos creados terminen...')
        for process in process_list:
            if process != process_list[0]:
                os.waitpid(process, 0)
        print('Todos los procesos han terminado, finalizando...')

if __name__ == '__main__':
    main()