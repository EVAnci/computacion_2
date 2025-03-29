import os

def main():
    pid = os.fork()

    if pid == 0:  # Proceso hijo
        print(f"Soy el hijo. Voy a ejecutar `git` para clonar un repositorio.")
        os.execlp("git", "git", "clone", "https://github.com/EVAnci/Notas")  # Reemplaza el proceso hijo con el comando `ls -l`
    else:
        os.wait()  # El padre espera que el hijo termine
        print("El hijo terminó de ejecutar `git clone`. El padre continúa.")

if __name__ == "__main__":
    main()
