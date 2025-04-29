# FEAT: Tobias Tkaczek

import os
import time

def create_child(child_number):
    child_number += 1 
    pid = os.fork()
    
    if pid == 0:  
        print(f"Soy el hijo {child_number}, mi PID es {os.getpid()}, el PID de mi padre es: {os.getppid()}")
        if child_number < 5:
            create_child(child_number)
        os._exit(0)

if __name__ == "__main__":
    os.system('clear')
    create_child(0)
    print(f"Soy el padre, mi PID es {os.getpid()}")