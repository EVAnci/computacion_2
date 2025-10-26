import argparse
import socketserver
import json
import logging
from concurrent.futures import ProcessPoolExecutor
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# --- Funciones de Tarea (CPU-Bound) ---
# Estas funciones se ejecutarán en el ProcessPoolExecutor

def run_full_analysis(url):
    """
    Función que se ejecuta en un proceso separado.
    Debe ser una función simple, no un método de clase,
    para que sea fácilmente "picklable".
    """
    log.info(f"[PID {os.getpid()}] Iniciando análisis para: {url}")
    try:
        # 1. Generar Screenshot
        # screenshot_b64 = take_screenshot(url)
        screenshot_b64 = f"base64_screenshot_for_{url}" # Mockup
        
        # 2. Análisis de Rendimiento
        # performance_data = analyze_performance(url)
        performance_data = {"load_time_ms": 1234, "total_size_kb": 567} # Mockup
        
        # 3. Análisis de Imágenes
        thumbnails = ["thumb1_b64", "thumb2_b64"] # Mockup
        
        log.info(f"[PID {os.getpid()}] Análisis completado para: {url}")
        
        return {
            "status": "success",
            "screenshot": screenshot_b64,
            "performance": performance_data,
            "thumbnails": thumbnails
        }
    except Exception as e:
        log.error(f"[PID {os.getpid()}] Error en análisis de {url}: {e}")
        return {"status": "error", "message": str(e)}

# ----------------------------------------

class TaskHandler(socketserver.BaseRequestHandler):
    """
    Manejador para cada conexión TCP al Servidor B.
    """
    
    def handle(self):
        try:
            # --- 1. Recibir datos ---
            # Usaremos un protocolo simple: 4 bytes (longitud) + JSON
            header = self.request.recv(4)
            if not header:
                return
            
            msg_len = int.from_bytes(header, 'big')
            data = self.request.recv(msg_len)
            
            task_data = json.loads(data.decode('utf-8'))
            log.info(f"Recibida tarea: {task_data}")

            # --- 2. Enviar tarea al Pool de Procesos ---
            # self.server.process_pool es el ProcessPoolExecutor
            future = self.server.process_pool.submit(
                run_full_analysis, 
                task_data['url']
            )
            
            # Obtenemos el resultado (esto bloquea ESTE HILO, 
            # pero no el servidor principal ni otros hilos)
            result = future.result() 

            # --- 3. Enviar respuesta ---
            response_data = json.dumps(result).encode('utf-8')
            response_header = len(response_data).to_bytes(4, 'big')
            
            self.request.sendall(response_header + response_data)
            
        except Exception as e:
            log.error(f"Error en TaskHandler: {e}", exc_info=True)
            try:
                # Intentar enviar un error de vuelta
                err_msg = json.dumps({"status": "error", "message": "Error interno del servidor B"}).encode('utf-8')
                err_header = len(err_msg).to_bytes(4, 'big')
                self.request.sendall(err_header + err_msg)
            except:
                pass # La conexión ya puede estar cerrada

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Servidor TCP que usa hilos para manejar cada conexión."""
    allow_reuse_address = True
    
    def __init__(self, server_address, RequestHandlerClass, process_pool):
        super().__init__(server_address, RequestHandlerClass)
        self.process_pool = process_pool

def main():
    DEFAULT_NUM_PROCESS = 4

    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument('-i', '--ip', required=True, help="Dirección de escucha")
    parser.add_argument('-p', '--port', required=True, type=int, help="Puerto de escucha")
    parser.add_argument('-n', '--processes', type=int, default=DEFAULT_NUM_PROCESS, 
                        help="Número de procesos en el pool (default: 4)")
    
    args = parser.parse_args()
    
    num_processes = args.processes if args.processes else DEFAULT_NUM_PROCESS
    log.info(f"Iniciando ProcessPoolExecutor con {num_processes} workers...")

    # Usamos un context manager para asegurar que el pool se cierre
    with ProcessPoolExecutor(max_workers=num_processes) as pool:
        server_address = (args.ip, args.port)
        
        # Pasamos el pool al constructor de nuestro servidor
        server = ThreadedTCPServer(
            server_address, 
            TaskHandler,
            process_pool=pool
        )
        
        log.info(f"Iniciando Servidor B en {args.ip}:{args.port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            log.info("Servidor B detenido manualmente.")
        finally:
            log.info("Cerrando servidor B...")
            server.shutdown()
            server.server_close()

if __name__ == "__main__":
    main()
