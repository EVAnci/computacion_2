from random import randint
import os, time
import fcntl

def random_sleep():
    sleep_time = randint(2,8)
    time.sleep(sleep_time)

def write_register_hi_level():
    with open("registro.txt",'a') as reg:
        reg.write(f'Proceso con PID: {os.getpid()} realizando escritura\n')

def write_register_with_lock():
    with open("registro.txt", 'a') as reg:
        fcntl.flock(reg, fcntl.LOCK_EX)  # Bloquea el archivo
        reg.write(f'Proceso con PID: {os.getpid()} realizando escritura\n')
        fcntl.flock(reg, fcntl.LOCK_UN)  # Libera el archivo

# flags recibe un entero: print(os.O_WRONLY | os.O_APPEND) -> 1025
def write_register_low_level():
    fd = os.open(path='registro.txt', flags=1025)
    message = f'Proceso con PID: {os.getpid()} realizando escritura\n'.encode()
    os.write(fd, message)
    os.close(fd)

def main():
    number_of_process = int(input('Numero de procesos a crear: '))

    children = []
    for i in range(number_of_process):
        pid = os.fork()
        if pid == 0:
            del children
            write_register_low_level()
            print(f'Proceso {i} - PID: {os.getpid()} durmiendo...')
            random_sleep()
            print(f'Proceso {i} - PID: {os.getpid()} terminado.')
            os._exit(0)
        else:
            children.append(pid)

    for child in children:
        os.waitpid(child, 0)
    print('Todos los procesos han finalizado. Terminando...')
    exit()

if __name__ == '__main__':
    main()