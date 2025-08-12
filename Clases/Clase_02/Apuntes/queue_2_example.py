from multiprocessing import Process, Queue, Event
import time

def hijo(q,r):
    print("[Hijo] Escribiendo en la cola...")
    q.put("Mensaje 1")
    q.put("Mensaje 2")
    
    time.sleep(2)  # Simula que el padre está ocupado

    r.wait()
    
    if not q.empty():
        print(f"[Hijo] Leyendo: {q.get()}")  # Se lee a sí mismo
        print(f"[Hijo] Leyendo: {q.get()}")  # Se lee a sí mismo
    print("[Hijo] Terminando.")

def padre(q,r):
    time.sleep(5)  # Simula que está ocupado y llega tarde

    if not q.empty():
        print(f"[Padre] Leyendo: {q.get()}")
        print(f"[Padre] Leyendo: {q.get()}")
    else:
        print("[Padre] No hay mensajes en la cola.")

    r.set()

if __name__ == "__main__":
    q = Queue()
    r = Event()
    
    p_hijo = Process(target=hijo, args=(q,r))
    p_padre = Process(target=padre, args=(q,r))

    p_hijo.start()
    p_padre.start()

    p_hijo.join()
    p_padre.join()
