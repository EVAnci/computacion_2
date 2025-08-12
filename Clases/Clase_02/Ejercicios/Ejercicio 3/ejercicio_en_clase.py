### Hagamos un programa que genere 5 hijos pero un padre pueda tener 1 hijo

import os
import time

def hijo(t):
    print(f"[Hijo] PID: {os.getpid()} - PPID: {os.getppid()} - Tiempo de espera {t}.")
    time.sleep(t)
    print(f'PID: {os.getpid()} - PPID: {os.getppid()} - Terminado')

def padre():
    for i in range(5):
        pid = os.fork()
        if pid != 0:
            hijo(1)
        break
    print(f"[Padre] PID: {os.getpid()}")
    if i != 4:
        os.wait()

if __name__ == "__main__":
    padre()
