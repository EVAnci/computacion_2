import os
import time

def main():
    pid = os.fork()

    if pid > 0:
        print(f"Soy el padre (PID: {os.getpid()}). No voy a hacer wait().")
        time.sleep(25)  # Simulamos que el padre sigue corriendo sin hacer wait()
        print("El padre terminó. Revisa si hubo un proceso zombi.")
    else:
        print(f"Soy el hijo (PID: {os.getpid()}). Terminando de inmediato.")
        exit(0)  # El hijo termina rápidamente

if __name__ == "__main__":
    main()
