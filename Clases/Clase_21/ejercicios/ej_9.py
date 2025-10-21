import asyncio

# Clientes con nc
# nc 127.0.0.1 9999

# Diccionario global para mantener a los clientes conectados
# La clave es el objeto 'writer' y el valor es el 'nombre'
clientes = {}  # {asyncio.StreamWriter: str}

async def broadcast(mensaje, remitente=None):
    """
    Envía un mensaje a todos los clientes conectados, excepto al remitente.
    """
    # Si no hay clientes, no hay nada que hacer
    if not clientes:
        return

    # Creamos una copia de las claves (writers) por si el diccionario
    # 'clientes' se modifica durante la iteración (alguien se desconecta)
    for writer in list(clientes.keys()):
        if writer == remitente:
            continue  # No enviar el mensaje de vuelta al remitente
        
        try:
            writer.write(mensaje.encode())
            await writer.drain()
        except (ConnectionResetError, BrokenPipeError):
            # El cliente se desconectó abruptamente.
            # Su propia tarea 'manejar_cliente' se encargará de
            # limpiarlo del diccionario 'clientes'.
            # No es necesario hacer nada aquí.
            pass

async def manejar_cliente(reader, writer):
    """
    Esta corrutina se ejecuta para cada cliente que se conecta.
    """
    addr = writer.get_extra_info('peername')
    print(f"Nueva conexión desde {addr}")
    
    nombre = None
    try:
        # 1. Pedir el nombre al cliente
        writer.write(b"Bienvenido al chat! Por favor, introduce tu nombre: ")
        await writer.drain()
        
        # Leer el nombre
        data = await reader.read(100)
        if not data:
            # El cliente se desconectó antes de enviar el nombre
            print(f"Cliente {addr} desconectado antes de identificarse.")
            return

        nombre = data.decode().strip()
        
        # Validar nombre (simple)
        if not nombre or nombre in clientes.values():
            writer.write(f"Nombre '{nombre}' no válido o ya está en uso. Desconectando.\n".encode())
            await writer.drain()
            print(f"Conexión rechazada para {addr}: nombre '{nombre}' inválido.")
            return

        # 2. Registrar al cliente y notificar a todos
        clientes[writer] = nombre
        writer.write(f"Hola, {nombre}! Eres bienvenido.\n".encode())
        writer.write(b"Escribe /list para ver usuarios o /quit para salir.\n")
        await writer.drain()
        
        print(f"{nombre} ({addr}) se ha unido al chat.")
        await broadcast(f"--- {nombre} se ha unido al chat ---\n", writer)

        # 3. Bucle principal: leer y procesar mensajes
        while True:
            data = await reader.read(1024)  # Leer hasta 1KB
            if not data:
                # El cliente cerró la conexión (ej. Ctrl+C en netcat)
                print(f"{nombre} ({addr}) ha cerrado la conexión (EOF).")
                break
            
            mensaje = data.decode().strip()
            
            # 4. Procesar comandos
            if mensaje == "/quit":
                print(f"{nombre} ha usado /quit.")
                break  # Salir del bucle while
            
            elif mensaje == "/list":
                lista_usuarios = ", ".join(clientes.values())
                writer.write(f"Usuarios conectados: {lista_usuarios}\n".encode())
                await writer.drain()
            
            elif mensaje:  # Ignorar líneas vacías
                # 3. Broadcast de mensajes normales
                mensaje_chat = f"<{nombre}> {mensaje}\n"
                await broadcast(mensaje_chat, writer)

    except asyncio.CancelledError:
        # La tarea fue cancelada (ej. el servidor se está apagando)
        print(f"Tarea para {nombre} ({addr}) cancelada.")
    except (ConnectionResetError, asyncio.IncompleteReadError) as e:
        # Desconexión abrupta
        print(f"Desconexión abrupta de {nombre} ({addr}): {e}")
    except Exception as e:
        # Otro error inesperado
        print(f"Error inesperado con {nombre} ({addr}): {e}")
    
    finally:
        # 5. Limpieza y notificación de salida
        # Esta sección se ejecuta SIEMPRE, ya sea por /quit,
        # desconexión abrupta, o error.
        
        # Solo si el cliente llegó a registrarse (tiene nombre)
        if writer in clientes:
            # Eliminar al cliente del diccionario
            del clientes[writer]
            
            # Notificar a los demás que el cliente se ha ido
            print(f"{nombre} ({addr}) ha abandonado el chat.")
            await broadcast(f"--- {nombre} ha abandonado el chat ---\n")
        
        # Cerrar la conexión
        if not writer.is_closing():
            writer.close()
            await writer.wait_closed()
        
        print(f"Conexión con {addr} cerrada.")

async def main():
    """
    Función principal para iniciar el servidor.
    """
    server = await asyncio.start_server(
        manejar_cliente, 
        '127.0.0.1', 
        9999
    )

    addr = server.sockets[0].getsockname()
    print(f"Servidor de chat iniciado en {addr}")
    print("Esperando conexiones...")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")