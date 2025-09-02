import socket

# Primero ejecutamos el servidor UDP
# nc -u -l 127.0.0.1 9006
#   -u es para protocolo sin conexión 

HOST, PORT = "127.0.0.1", 9006

# Ojo: Acá se define un socket udp
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"ping", (HOST, PORT))
    data, addr = s.recvfrom(2048) # Tamaño máximo del datagrama
    print(f"< {data!r} desde {addr}")
    # < b'pong\n' desde ('127.0.0.1', 9006)
