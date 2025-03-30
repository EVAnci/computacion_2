import multiprocessing
import time
import random
import os

def auto(nombre, estacionamiento, lock, evento):
    """Simula un auto que intenta estacionar y salir después de un tiempo."""
    
    with lock:
        print(f"🚗 {nombre} está intentando ingresar. PID: {os.getpid()}")

    estacionamiento.acquire()  # Esperar un espacio libre
    with lock:
        print(f"✅ {nombre} ha ingresado al estacionamiento. Espacios libres: {estacionamiento.get_value()}")
    
    time.sleep(random.randint(5,10))  # Simula el tiempo estacionado
    
    with lock:
        print(f"⛔ {nombre} ha salido del estacionamiento.")
    estacionamiento.release()  # Liberar espacio
    
    if estacionamiento.get_value() == 3:  # Si el estacionamiento se vacía, activamos el evento
        evento.set()

def monitor(evento, lock):
    """Monitorea si el estacionamiento se ha llenado y envía una notificación."""
    while True:
        evento.wait()  # Espera a que el evento se active (cuando el estacionamiento esté vacío)
        with lock:
            print("🚦 El estacionamiento está completamente vacío. Se pueden ingresar nuevos autos.")
        evento.clear()  # Resetear el evento para la siguiente detección

if __name__ == "__main__":
    lock = multiprocessing.Lock()
    evento = multiprocessing.Event()
    estacionamiento = multiprocessing.Semaphore(3)  # Solo 3 autos pueden entrar al mismo tiempo
    
    autos = ["Auto-1", "Auto-2", "Auto-3", "Auto-4", "Auto-5", "Auto-6"]
    
    monitor_proceso = multiprocessing.Process(target=monitor, args=(evento, lock))
    monitor_proceso.daemon = True  # Proceso en segundo plano
    monitor_proceso.start()

    procesos = []
    for nombre in autos:
        p = multiprocessing.Process(target=auto, args=(nombre, estacionamiento, lock, evento))
        procesos.append(p)
        p.start()
        time.sleep(random.uniform(0.5, 1.5))  # Retraso aleatorio en la llegada de autos
    
    for p in procesos:
        p.join()  # Esperar a que todos los autos terminen

    print("🏁 Simulación finalizada.")
