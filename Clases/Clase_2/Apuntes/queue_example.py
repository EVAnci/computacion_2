import multiprocessing
import time

def worker(queue):
    """Función ejecutada por el proceso hijo."""
    for i in range(5):
        message = f"Mensaje {i} desde el proceso hijo"
        queue.put(message)  # Envía un mensaje a la cola
        time.sleep(1)
    queue.put('listo')
    time.sleep(1)
    print(f'El proceso hijo recibió: {queue.get()}')

if __name__ == "__main__":
    queue = multiprocessing.Queue()  # Crear una cola compartida
    process = multiprocessing.Process(target=worker, args=(queue,))
    
    process.start()  # Iniciar proceso hijo
    msg = ''
    time.sleep(2)
    # El proceso padre recibe los mensajes de la cola
    while process.is_alive() or not queue.empty():
        while not queue.empty():
            msg = queue.get()  # Obtener mensaje de la cola
            print(f"Proceso padre recibió: {msg}")
        if msg == 'listo':
            break

    queue.put("Soy el proceso padre, veamos si el hijo recibe el mensaje...")
    
    process.join()  # Esperar a que el proceso hijo termine
    print("El proceso hijo ha terminado.")
