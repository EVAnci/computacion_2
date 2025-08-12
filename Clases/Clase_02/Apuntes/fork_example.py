import os

def main():
    print('Se ejecuta de forma normal')
    print(f'PID: {os.getpid()}') 
    input('Presiona Enter para continuar...')
    pid = os.fork()
    
    if pid > 0:
        print(f"Soy el proceso padre. Mi PID es {os.getpid()} y mi hijo tiene PID {pid}. La función fork() devuelve {pid}")
    else:
        print(f"Soy el proceso hijo. Mi PID es {os.getpid()} y mi padre tiene PID {os.getppid()}. La función fork() devuelve {pid}")

if __name__ == "__main__":
    main()