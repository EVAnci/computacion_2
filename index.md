## Índice consolidado de temas

### 1. Entorno de desarrollo y herramientas básicas

**Contexto:** herramientas necesarias para desarrollar y ejecutar programas desde Unix/Linux y Python.

* Control de versiones con **Git**

  * repositorios, commits, staging area, branches y remotes
  * modelo distribuido y snapshots
  * flujos de trabajo con ramas
* Entrada/Salida en **Unix/Linux**

  * `stdin`, `stdout`, `stderr`
  * descriptores de archivo
  * redirecciones
  * pipes de shell
  * dispositivos `/dev/*`
* Programas de línea de comandos en **Python**

  * `sys.argv`
  * `getopt`
  * `argparse`
  * parámetros posicionales/opcionales, validación y ayuda automática.   

### 2. Procesos y modelo de ejecución del sistema operativo

**Contexto:** fundamentos de Sistemas Operativos, especialmente el modelo Unix, utilizando luego Python para experimentar.

* Programa vs. proceso
* PID / PPID y jerarquía de procesos
* estados y ciclo de vida
* memoria y recursos de un proceso
* planificación y multiprogramación
* `fork()`
* `exec()`
* copy-on-write
* procesos padre/hijo
* procesos zombis y huérfanos
* `wait()` / recolección de procesos
* modelo Unix/Linux y `/proc`.  

### 3. Comunicación entre procesos — IPC

**Contexto:** mecanismos que permiten comunicar procesos aislados dentro de una máquina Unix/Linux.

* concepto general de **IPC**
* pipes anónimos

  * `pipe()`
  * extremos de lectura/escritura
  * buffers
  * bloqueo
  * EOF
  * herencia mediante `fork()`
  * `os.pipe()` en Python
* FIFOs / named pipes

  * `mkfifo`
  * persistencia en filesystem
  * procesos no relacionados
  * modo bloqueante / `O_NONBLOCK`
  * `select()` / `poll()`
* patrones productor-consumidor
* comunicación unidireccional y bidireccional
* señales Unix/POSIX

  * `SIGINT`, `SIGUSR*`, etc.
  * handlers
  * máscaras y bloqueo
  * `kill`, `sigaction`, `sigwait`
  * señales en Python con `signal`.   

### 4. Concurrencia, paralelismo e hilos

**Contexto:** cómo ejecutar múltiples flujos de trabajo y cómo elegir entre hilos, procesos y corrutinas en Python.

* concurrencia vs. paralelismo
* hilos vs. procesos
* memoria compartida vs. memoria aislada
* hilos de usuario vs. hilos del kernel
* multitarea preventiva vs. cooperativa
* cambio de contexto
* tareas **CPU-bound** vs. **I/O-bound**
* módulo Python `threading`
* creación y finalización de threads
* `start()` / `join()`
* daemon threads
* Global Interpreter Lock (**GIL**)
* comparación:

  * `threading`
  * `multiprocessing`
  * `asyncio`.   

### 5. Multiprocessing y sincronización

**Contexto:** uso de múltiples procesos Python para obtener paralelismo real y coordinar recursos compartidos.

* módulo `multiprocessing`
* `Process`
* `start`, `join`, `is_alive`
* GIL y paralelismo multiproceso
* IPC con:

  * `Pipe`
  * `Queue`
* condiciones de carrera
* secciones críticas
* exclusión mutua
* deadlocks
* primitivas de sincronización:

  * `Lock`
  * `RLock`
  * `Semaphore`
  * `BoundedSemaphore`
  * `Condition`
  * `Event`
  * `Barrier`
* datos compartidos:

  * `Value`
  * `Array`
* patrones productor-consumidor y workers.    

---

# Redes

### 6. Fundamentos de redes de computadoras

**Contexto:** base conceptual previa a programar comunicaciones de red.

* concepto de red
* LAN / WAN
* topologías
* conmutación de paquetes
* historia de ARPANET e Internet
* arquitectura en capas
* modelo **OSI**
* modelo **TCP/IP**
* encapsulamiento
* direccionamiento
* puertos
* multiplexación
* transporte y aplicaciones
* RFCs y estandarización de protocolos.  

### 7. TCP, UDP y sockets

**Contexto:** programación de redes directamente con la biblioteca estándar `socket` de Python.

* sockets como abstracción de comunicación
* modelo cliente-servidor
* TCP / `SOCK_STREAM`

  * conexión
  * `bind`
  * `listen`
  * `accept`
  * `connect`
  * `send` / `sendall`
  * `recv`
* UDP / `SOCK_DGRAM`

  * `sendto`
  * `recvfrom`
* servidores secuenciales
* servidores Echo
* protocolos textuales simples
* framing de mensajes en TCP
* lecturas parciales
* EOF y cierre de conexión
* `shutdown`
* timeouts
* reintentos
* broadcast UDP
* resolución con `getaddrinfo`.   

### 8. Unix Domain Sockets

**Contexto:** uso de sockets para IPC local en sistemas Unix/Linux.

* `AF_UNIX`
* `SOCK_STREAM`
* `SOCK_DGRAM`
* paths de sockets
* abstract namespace de Linux
* credenciales del proceso remoto con `SO_PEERCRED`
* transferencia de descriptores mediante `SCM_RIGHTS`. 

### 9. IPv4 e IPv6

**Contexto:** direccionamiento IP aplicado luego a sockets Python.

* IPv4 vs. IPv6
* agotamiento de IPv4 y evolución hacia IPv6
* direcciones IPv6 de 128 bits
* representación hexadecimal
* reglas de compresión
* unicast
* multicast
* anycast
* link-local / global
* encabezado IPv6
* extension headers
* ICMPv6
* Neighbor Discovery
* SLAAC / autoconfiguración
* `AF_INET` vs. `AF_INET6`
* sockets TCP IPv6
* `getaddrinfo`
* IPv4-mapped IPv6
* **dual-stack**
* `IPV6_V6ONLY`.   

### 10. Herramientas de diagnóstico y experimentación de red

**Contexto:** interacción manual con protocolos antes o durante su implementación en Python.

* `telnet`
* `netcat` / `nc`

  * cliente TCP
  * servidor TCP
  * UDP
  * pruebas de puertos
* `dig`
* DNS

  * A
  * AAAA
  * MX
  * NS
  * TXT
* pruebas manuales de protocolos de texto.  

### 11. Protocolos de capa de aplicación

**Contexto:** se pasa de sockets genéricos a protocolos estandarizados.

* HTTP
* DNS
* SMTP
* Daytime
* modelo request/response
* protocolos definidos mediante RFCs
* experimentación con clientes manuales
* implementación de protocolos sencillos sobre TCP/UDP.  

### 12. HTTP y servidores web en Python

**Contexto:** construcción de servidores de capa de aplicación sobre TCP.

* HTTP como protocolo stateless
* request / response
* métodos:

  * GET
  * POST
  * PUT
  * DELETE
  * HEAD
  * PATCH
  * OPTIONS
* códigos 2xx / 3xx / 4xx / 5xx
* headers HTTP
* módulo `http.server`
* `HTTPServer`
* `ThreadingHTTPServer`
* `SimpleHTTPRequestHandler`
* `BaseHTTPRequestHandler`
* handlers personalizados
* routing básico
* respuestas HTML / JSON.   

### 13. Framework `socketserver`

**Contexto:** abstracción de nivel superior para dejar de gestionar sockets manualmente.

* `BaseServer`
* `TCPServer`
* `UDPServer`
* `UnixStreamServer`
* `UnixDatagramServer`
* `BaseRequestHandler`
* handlers
* `serve_forever`
* concurrencia mediante:

  * `ThreadingMixIn`
  * `ForkingMixIn`
* servidores secuenciales vs. threaded vs. forked
* combinación de TCP, UDP y HTTP.  

---

# Contenedores y despliegue

### 14. Docker y contenedorización

**Contexto:** llevar los programas y servicios anteriores a entornos aislados y reproducibles.

* virtualización vs. contenedores
* imágenes y contenedores
* Docker Engine
* Docker daemon / CLI / API
* `containerd` / `runc`
* namespaces
* cgroups
* filesystem por capas / copy-on-write
* Dockerfile
* construcción de imágenes
* registries
* multi-stage builds
* ciclo de vida de contenedores
* almacenamiento y volúmenes
* networking Docker
* Docker Compose
* aplicaciones multi-contenedor
* seguridad
* logs, troubleshooting y debugging.  

### 15. Laboratorio de servicios con Docker Compose

**Contexto:** stack práctico para observar protocolos reales.

* Echo HTTP
* Daytime
* SMTP con MailHog
* DNS con `dig`
* TCP/UDP con Netcat
* puertos y mapeos
* levantar/detener servicios con `docker compose`.  

---

# Programación asíncrona y procesamiento de tareas

### 16. Generadores y `yield`

**Contexto:** punto conceptual de entrada hacia la concurrencia cooperativa de Python.

* generadores
* evaluación perezosa
* `yield`
* `next()`
* `StopIteration`
* preservación del estado de ejecución
* pipelines de datos
* `.send()`
* proto-corrutinas
* scheduler cooperativo sencillo.  

### 17. `asyncio`

**Contexto:** concurrencia cooperativa orientada principalmente a operaciones I/O-bound.

* corrutinas
* event loop
* green threads
* `async def`
* `await`
* awaitables
* Tasks / Futures
* `asyncio.run`
* operaciones bloqueantes vs. no bloqueantes
* `asyncio.sleep`
* relación conceptual `yield` → corrutinas → `async/await`
* ejecución concurrente de operaciones de red.  

### 18. `concurrent.futures`

**Contexto:** API de alto nivel para usar pools de threads o procesos sin gestionar manualmente cada worker.

* `ThreadPoolExecutor`
* `ProcessPoolExecutor`
* CPU-bound vs. I/O-bound
* GIL
* `Future`
* `submit`
* `map`
* `as_completed`
* obtención de resultados y excepciones
* cancelación
* timeouts
* callbacks
* procesamiento por chunks
* pools de workers
* límites de recursos
* procesamiento paralelo de archivos/datos.  

### 19. Celery y tareas distribuidas

**Contexto:** evolución desde concurrencia local hacia ejecución de tareas persistentes y distribuida entre varias máquinas.

* task queues
* productores y workers
* message broker
* Redis
* RabbitMQ
* result backend
* `AsyncResult`
* estados de una tarea
* serialización
* escalabilidad horizontal
* persistencia
* resiliencia
* scheduling
* firmas de tareas
* composición:

  * chains
  * groups
  * chords
* monitoreo con Flower
* inspección de workers
* logging
* idempotencia
* timeouts
* buenas prácticas de producción.   

## En una línea: recorrido conceptual

**Unix/Linux y Git → procesos → IPC → hilos y multiprocessing → sincronización → redes y TCP/IP → sockets → TCP/UDP/IPv4/IPv6 → HTTP y servidores → Docker → `yield`/`asyncio` → `concurrent.futures` → Celery y sistemas distribuidos.**
