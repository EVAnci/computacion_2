from random import randint
import os, time

def random_sleep():
    random_number = randint(1,8)
    print(f'PID: {os.getpid()}; PPID: {os.getppid()} - Esperaré {random_number} segundos...')
    time.sleep(random_number)
    print(f'PID: {os.getpid()} y he despertado!')

def main():
    number_of_process = int(input('Escribe el número de procesos a crear: '))

    print(f'Soy el proceso principal. PID: {os.getpid()}')

    children = []
    for i in range(number_of_process):
        pid = os.fork()
        if pid == 0:
            del children
            print(f'Soy el proceso hijo {i+1}. ', end='')
            random_sleep()
            os._exit(0)
        else:
            children.append(pid)

    if children:
        print(f'Esperando a que los procesos con PID: {children} terminen...')
        for child in children:
            os.waitpid(child, 0)
        print('Todos los procesos han finalizado correctamente. Terminando...')
        exit() # Salgo con exit de python que aplica una limpieza antes de matar el proceso

if __name__ == '__main__':
    main()