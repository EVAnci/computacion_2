import os
import time

def hijo():
    print(f"[Hijo] PID: {os.getpid()} terminando.")
    os._exit(0)  # El hijo termina inmediatamente

def padre():
    pid = os.fork()
    if pid == 0:
        hijo()
    else:
        print(f"[Padre] PID: {os.getpid()}, hijo creado con PID: {pid}")
        time.sleep(5)  # Simulamos que el padre está ocupado

        # Mostramos los procesos zombi en el sistema
        os.system(f"ps -o pid,ppid,stat,cmd | grep {pid}")

        print("[Padre] Saliendo sin recoger el estado del hijo.")

if __name__ == "__main__":
    padre()
