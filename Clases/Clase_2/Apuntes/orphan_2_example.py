import os, time

def hijo_huerfano():
    time.sleep(3)  # Simula un hijo que tarda más en terminar
    print(f"[Hijo] Soy {os.getpid()}, mi nuevo padre es {os.getppid()}")

def crear_huerfano():
    pid = os.fork()
    if pid == 0:
        hijo_huerfano()
        os._exit(0)
    else:
        print(f"[Padre] PID: {os.getpid()}, hijo creado con PID: {pid}")
        print("[Padre] Terminando antes que el hijo.")
        os._exit(0)  # El padre finaliza

if __name__ == "__main__":
    crear_huerfano()
    time.sleep(5)  # Para que veamos el mensaje del hijo
