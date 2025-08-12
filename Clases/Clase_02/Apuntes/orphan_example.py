import os
import time

def main():
    print('Se ejecuta de forma normal')
    print(f'PID: {os.getpid()} - PID del padre: {os.getppid()} (python)')
    pid = os.fork()

    if pid > 0:
        print(f"Soy el padre (PID: {os.getpid()}), terminando antes que el hijo.")
        exit(0)  # El padre finaliza antes que el hijo
    else:
        print(f"Soy el hijo (PID: {os.getpid()}), mi padre era {os.getppid()}.")
        time.sleep(3)  # Simulamos que el hijo sigue ejecutándose
        print(f"Ahora mi nuevo padre es {os.getppid()} (init/systemd).")

if __name__ == "__main__":
    main()
