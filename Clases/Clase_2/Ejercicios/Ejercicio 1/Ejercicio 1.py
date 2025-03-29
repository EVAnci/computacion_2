import os
import time

def main():
    process_list = []

    process_list.append(os.fork())
    if process_list[0] > 0:
        process_list.append(os.fork())
        if process_list[1] > 0:
            process_list.append(os.fork())
            if process_list[2] > 0:
                print(f'Soy el proceso padre - PID: {os.getpid()}; espero a que los procesos hijos terminen.')
                os.wait()
                print('Todos los procesos han terminado. Saliendo...')

    if process_list[-1] == 0:
        time.sleep(2)
        print(f'Soy un proceso hijo - PID: {os.getpid()}; PPID: {os.getppid()}')        


if __name__ == '__main__':
    main()