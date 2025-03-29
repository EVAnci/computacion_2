import os
import time

def main():
    pid = os.fork()

    if pid > 0:
        print(f"Padre esperando que el hijo ({pid}) termine...")
        os.wait()  # El padre espera a que el hijo termine
        print("El hijo ha terminado. El padre continúa.")
    else:
        print(f"Soy el hijo. Mi PID es {os.getpid()}")
        time.sleep(2)  # Simulamos una tarea del hijo
        print("Hijo terminando.")

if __name__ == "__main__":
    main()