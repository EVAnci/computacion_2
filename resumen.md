# Resumen

# Pipes

## ¿Qué es un pipe?

Un pipe (o "tubería") es un mecanismo de comunicación unidireccional entre procesos que permite que la salida de un proceso se utilice como entrada de otro. Su uso está muy relacionado con el principio de composición de procesos, común en sistemas UNIX y Linux.

## Características principales
- Comunicación unidireccional: un extremo escribe, el otro lee.
- Los pipes tradicionales (anónimos) solo funcionan entre procesos con un ancestro común (por ejemplo, padre-hijo).
- Existe también la variante named pipe (FIFO), que permite comunicación entre procesos no relacionados directamente.

## Implementación de Pipes en Python

Para trabajar con pipes en Python, se puede usar:

- `os.pipe()`: para crear pipes de bajo nivel, similar a C.
- `multiprocessing.Pipe()`: para comunicación entre procesos usando la librería multiprocessing.

## Paso a paso con os.pipe()

1. Crear el pipe
    ```py
    import os

    r, w = os.pipe()  # r: descriptor de lectura, w: descriptor de escritura

        Bifurcar el proceso

    pid = os.fork()
    ```

2. Gestionar extremos según el proceso
    ```py
    if pid == 0:
        # Proceso hijo (escribe)
        os.close(r)  # Cierra lectura
        w_fd = os.fdopen(w, 'w')  # Abre descriptor como archivo para escribir
        w_fd.write("Hola desde el hijo\n")
        w_fd.close()
    else:
        # Proceso padre (lee)
        os.close(w)  # Cierra escritura
        r_fd = os.fdopen(r)  # Abre descriptor como archivo para leer
        print("Padre lee:", r_fd.read())
        r_fd.close()
    ```

>📌 Este ejemplo ilustra la comunicación unidireccional clásica entre un padre que lee y un hijo que escribe. La sincronización implícita ocurre porque read() bloquea hasta que el hijo termina de escribir y cierra el descriptor.

## Pipeline

Un pipeline es cuando la salida de un proceso se conecta como entrada del siguiente, tal como en:
```bash
ls | grep ".py" | sort
```
Vamos a replicar algo similar en Python: tres procesos que simulan este encadenamiento.

📄 **Ejemplo: pipeline de 3 procesos**

Objetivo: Proceso A genera datos → Proceso B los transforma → Proceso C los muestra

```py
import os

# Creamos dos pipes: A->B y B->C
r1, w1 = os.pipe()  # Pipe entre A y B
r2, w2 = os.pipe()  # Pipe entre B y C

pid_a = os.fork()
if pid_a == 0:
    # Proceso A (escribe al pipe1)
    os.close(r1)
    os.close(r2)
    os.close(w2)
    w1_fd = os.fdopen(w1, 'w')
    w1_fd.write("uno\ndos\ntres\n")
    w1_fd.close()
    exit()

pid_b = os.fork()
if pid_b == 0:
    # Proceso B (lee de pipe1, escribe en pipe2)
    os.close(w1)
    os.close(r2)
    r1_fd = os.fdopen(r1)
    w2_fd = os.fdopen(w2, 'w')
    for line in r1_fd:
        w2_fd.write(line.upper())  # Transforma a mayúsculas
    r1_fd.close()
    w2_fd.close()
    exit()

# Proceso C (padre)
os.close(w1)
os.close(w2)
os.close(r1)
r2_fd = os.fdopen(r2)
print("Proceso C recibe:")
for line in r2_fd:
    print(line.strip())
r2_fd.close()
```

---

# FIFOs en Sistemas Unix/Linux: Fundamentos, Implementación y Aplicaciones Avanzadas

## Introducción

En el ecosistema Unix/Linux, los mecanismos de comunicación entre procesos (IPC, por sus siglas en inglés) constituyen una piedra angular del diseño de sistemas operativos robustos y eficientes. Entre estos mecanismos, los *FIFOs* (First-In-First-Out), también conocidos como *named pipes*, ofrecen una forma elegante y persistente de intercambio de datos unidireccional o bidireccional entre procesos no emparentados. Este documento aborda en profundidad el modelo FIFO, desde su fundamentación teórica y evolución histórica hasta su implementación en el kernel, acompañado de ejemplos prácticos y análisis comparativos.

## 2. Fundamentos Teóricos

### 2.1 Comunicación entre procesos: panorama general

La comunicación entre procesos es necesaria para lograr cooperación, coordinación y compartición de información. Unix ofrece diversos mecanismos: pipes anónimos y FIFOs. La elección depende de factores como persistencia, necesidad de bloqueo, estructura de datos y requisitos de sincronización.

### 2.2 El modelo FIFO: principios y características

Un FIFO es un archivo especial que actúa como canal de comunicación. Su característica principal es que el primer byte escrito es el primero en ser leído, garantizando un orden de llegada (semántica FIFO). A diferencia de un pipe anónimo, un FIFO tiene una entrada en el sistema de archivos, lo que lo hace accesible por procesos no relacionados y persistente entre ejecuciones.

## 3. Contexto Histórico

### 3.1 Evolución de los mecanismos IPC en sistemas Unix

Los primeros sistemas Unix (Bell Labs, década de 1970) incorporaban *pipes* como mecanismos de comunicación unidireccional entre procesos relacionados. Sin embargo, esto limitaba su aplicabilidad. Con la introducción de los *named pipes* en System III y posteriormente System V, se amplió el paradigma IPC a procesos disociados, permitiendo arquitecturas más flexibles.

### 3.2 De pipes anónimos a named pipes

Mientras los pipes anónimos requieren herencia del descriptor de archivo (normalmente vía fork), los FIFOs pueden ser accedidos por cualquier proceso con los permisos adecuados. Esta independencia favoreció diseños más desacoplados y modulares.

## 4. Arquitectura Interna

### 4.1 Implementación a nivel de kernel

El kernel trata los FIFOs como archivos especiales con semántica de buffer circular. Están asociados a una estructura `inode` y gestionan la cola de bytes mediante `pipe_inode_info`. Internamente, usan mecanismos de sincronización como *wait queues* para gestionar la espera de procesos lectores y escritores. Los accesos se coordinan para evitar condiciones de carrera.

### 4.2 Estructuras de datos y buffers

Los FIFOs utilizan una región de memoria en el espacio del kernel para almacenar los datos temporalmente. Su tamaño suele ser configurable a nivel de sistema (`/proc/sys/fs/pipe-max-size`) y se implementa como una cola circular. Esta estructura permite evitar copias innecesarias y reducir la latencia.

### 4.3 Sincronización y bloqueo

Si un proceso intenta leer un FIFO vacío, quedará bloqueado hasta que haya datos. Igualmente, un proceso que escribe puede ser bloqueado si no hay lectores. Alternativamente, pueden usarse las flags `O_NONBLOCK` para evitar esta espera. El kernel sincroniza ambos extremos y administra correctamente los estados de espera.

## 5. Operaciones Fundamentales

### 5.1 Creación de FIFOs

La llamada al sistema `mkfifo(const char *pathname, mode_t mode)` o el comando `mkfifo` permite crear un FIFO persistente:

```bash
$ mkfifo /tmp/mi_fifo
```

Este archivo especial puede ser abierto por múltiples procesos para escritura o lectura.

### 5.2 Mecanismos de lectura y escritura (modo bajo nivel con `os`)

La lectura y escritura en un FIFO puede realizarse no solo con la función `open()` de alto nivel en Python, sino también utilizando la librería `os`, que permite trabajar con descriptores de archivo y banderas POSIX de forma más cercana al sistema operativo. Esto es útil cuando se requiere control fino sobre bloqueo, apertura no bloqueante, o tratamiento explícito de errores.

---

### Ejemplo básico con `os.open`, `os.read`, `os.write`

Antes de ejecutar estos scripts, crear el FIFO desde terminal:

```bash
mkfifo /tmp/mi_fifo
```

#### Escritura:
```python
# escribir_fifo_os.py
import os
import time

fd = os.open('/tmp/mi_fifo', os.O_WRONLY)
os.write(fd, b'Hola desde os.write\n')
os.close(fd)
```

#### Lectura:
```python
# leer_fifo_os.py
import os

fd = os.open('/tmp/mi_fifo', os.O_RDONLY)
data = os.read(fd, 1024)
print('Lectura:', data.decode())
os.close(fd)
```

---

### Control de bloqueo con `O_NONBLOCK`

Con `O_NONBLOCK`, es posible evitar que el proceso quede bloqueado si no hay otro extremo abierto todavía.

```python
# lector_no_block.py
import os
import errno
import time

try:
    fd = os.open('/tmp/mi_fifo', os.O_RDONLY | os.O_NONBLOCK)
    data = os.read(fd, 1024)
    print('Leído:', data.decode() if data else '[sin datos]')
    os.close(fd)
except OSError as e:
    if e.errno == errno.ENXIO:
        print('No hay escritor disponible aún.')
```

---

### Comportamiento del cursor y consumo de datos

A diferencia de un archivo tradicional, en un FIFO **los datos se consumen en la lectura**. Esto significa que **no pueden ser leídos nuevamente por otro proceso**, aunque cada uno tenga su propio descriptor de archivo.

Ejemplo:

```bash
mkfifo /tmp/fifo_cursor_os
```

```python
# escribir_fifo_cursor_os.py
import os

fd = os.open('/tmp/fifo_cursor_os', os.O_WRONLY)
os.write(fd, b'ABCDEF')
os.close(fd)
```

```python
# lector_1_os.py
import os

fd = os.open('/tmp/fifo_cursor_os', os.O_RDONLY)
print('Lector 1 lee:', os.read(fd, 3).decode())  # ABC
os.close(fd)
```

```python
# lector_2_os.py
import os

fd = os.open('/tmp/fifo_cursor_os', os.O_RDONLY)
print('Lector 2 lee:', os.read(fd, 3).decode())  # DEF o vacío si ya se consumió
os.close(fd)
```

> Como los datos ya fueron consumidos por el primer lector, el segundo proceso lee solo los restantes, o nada si el buffer ya se vació. Esto demuestra que en un FIFO los datos **no persisten** y el **acceso es secuencial y destructivo**.

---

Este modo de trabajo con `os` y descriptores de archivo es fundamental para aplicaciones que requieren operaciones sin bloqueo, multiplexado con `select()`, o integración con estructuras de bajo nivel del sistema operativo.

### 5.3 Llamadas del sistema relacionadas

- `open()`
- `read()` / `write()`
- `close()`
- `mkfifo()`
- `select()` / `poll()` (para detección de disponibilidad)

## 6. Patrones de Implementación

### 6.1 Modelo productor-consumidor

Uno o más procesos escriben datos que otros procesos consumen. La FIFO garantiza orden y aislamiento entre productores y consumidores. El buffer interno actúa como zona crítica.

### 6.2 Comunicación unidireccional

Un FIFO puede ser leído por un proceso y escrito por otro. Ideal para flujos de datos simples donde no se necesita respuesta.

### 6.3 Comunicación bidireccional

Se crea un par de FIFOs (ej: `/tmp/fifo_in`, `/tmp/fifo_out`) para lograr ida y vuelta, replicando un canal de duplexidad básica. Se requiere cuidado para evitar deadlocks.

## 7. Comparativa con Otros Mecanismos IPC

### 7.1 FIFOs vs Pipes anónimos

| Característica     | FIFO                   | Pipe anónimo            |
|--------------------|------------------------|--------------------------|
| Persistencia       | Sí                     | No                       |
| Acceso             | Procesos no relacionados | Solo procesos relacionados |
| Ubicación          | Sistema de archivos    | Descriptores de archivo  |
| Supervisión externa| Posible con `ls`, `stat`| No visible               |

## 8. Análisis de Rendimiento

### 8.1 Factores que afectan la latencia

- Tamaño del buffer FIFO
- Frecuencia de lectura/escritura
- Prioridad y afinidad de los procesos
- Carga del sistema y contenido del buffer

### 8.2 Consideraciones sobre el throughput

La transferencia sostenida depende de la eficiencia del buffer y el scheduler de procesos. El uso de `select()` o `poll()` puede optimizar la disponibilidad de lectura sin bloqueo activo.

### 8.3 Limitaciones y tamaño de buffer

El tamaño máximo está limitado por la configuración del sistema. El uso excesivo puede llevar a cuellos de botella si los consumidores no vacían la cola con suficiente rapidez.

## 9. Implementaciones Prácticas

### 9.1 Comunicación básica entre procesos

```python
# escritor.py
with open('/tmp/canal', 'w') as fifo:
    fifo.write('Mensaje enviado\n')
```

```python
# lector.py
with open('/tmp/canal', 'r') as fifo:
    print('Receptor:', fifo.readline())
```

### 9.2 Implementación de un sistema de log

```python
# logger.py
with open('/tmp/log_fifo', 'r') as fifo, open('registro.log', 'a') as log:
    for line in fifo:
        log.write(line)
```


---

# Queues (multiprocessing)

Instrucciones detalladas para implementar Queues en Python
En Python, la forma más común y segura de usar Queues para comunicación entre procesos es a través del módulo multiprocessing. Este módulo abstrae muchos detalles complejos y permite una implementación clara y eficiente.

## Herramienta principal: multiprocessing.Queue
Este objeto actúa como una cola de mensajes compartida entre procesos. Internamente utiliza un pipe y mecanismos de sincronización para garantizar la seguridad de los datos.

## Estructura básica
```py
from multiprocessing import Process, Queue

def productor(queue):
    for i in range(5):
        queue.put(f"Dato {i}")
        print(f"Productor puso: Dato {i}")

def consumidor(queue):
    while not queue.empty():
        dato = queue.get()
        print(f"Consumidor recibió: {dato}")

if __name__ == "__main__":
    q = Queue()

    p1 = Process(target=productor, args=(q,))
    p2 = Process(target=consumidor, args=(q,))

    p1.start()
    p1.join()  # Esperamos a que termine de poner datos

    p2.start()
    p2.join()  # Esperamos a que consuma todo
```

**Detalles importantes:**
- queue.put(dato) añade un elemento.
- queue.get() lo extrae.
- queue.empty() comprueba si la cola está vacía (aunque no es 100% confiable si hay concurrencia activa).
- join() espera a que el proceso termine.
- El código debe estar dentro del `if __name__ == "__main__"` para evitar problemas en Windows

# Pipe (multiprocessing)

La función `multiprocessing.Pipe()` en Python permite crear un **canal de comunicación bidireccional** entre dos procesos. Este canal se implementa mediante un par de **extremos conectados** llamados **conexiones** (`Connection` objects). Es útil cuando deseas que dos procesos (por ejemplo, un padre y su hijo) puedan intercambiar datos de forma directa.

## Funcionamiento general

Cuando invocas `multiprocessing.Pipe()`, se devuelve una **tupla con dos objetos** de tipo `Connection`, por ejemplo:

```python
conn1, conn2 = multiprocessing.Pipe()
```

Ambos extremos del pipe permiten enviar y recibir datos usando los métodos:

* `send(obj)`: envía un objeto a través del pipe.
* `recv()`: recibe un objeto desde el otro extremo del pipe.

### Ejemplo básico

```python
from multiprocessing import Process, Pipe

def child(conn):
    conn.send("Mensaje desde el hijo")
    respuesta = conn.recv()
    print("Hijo recibió:", respuesta)

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()

    p = Process(target=child, args=(child_conn,))
    p.start()

    print("Padre recibió:", parent_conn.recv())
    parent_conn.send("Hola hijo")
    p.join()
```

**Salida esperada:**

```
Padre recibió: Mensaje desde el hijo
Hijo recibió: Hola hijo
```

## Características importantes

* **Bidireccionalidad:** Por defecto, ambos extremos pueden enviar y recibir. Si deseas un pipe **unidireccional**, puedes pasar `duplex=False` al constructor, y entonces:

  * El primer extremo solo podrá **enviar**.
  * El segundo extremo solo podrá **recibir**.

  Ejemplo:

  ```python
  send_conn, recv_conn = Pipe(duplex=False)
  ```

* **Serialización automática:** Los objetos enviados por `send` se serializan usando `pickle`. Por tanto, puedes enviar cualquier objeto que sea "pickleable".

* **Bloqueo implícito:** Las operaciones `recv()` se bloquean hasta que se recibe algo. Para evitar bloqueos, podés usar `conn.poll(timeout)` para verificar si hay algo que leer.

### Comparación con `Queue`

Aunque `Pipe` es útil para **comunicación directa entre dos procesos**, para situaciones más complejas (por ejemplo, varios productores/consumidores) es preferible `multiprocessing.Queue()`, que es más flexible y está basada en colas seguras entre procesos.

Si necesitás un ejemplo específico de comunicación entre varios procesos usando `Pipe`, o querés ver cómo se diferencia internamente de otros mecanismos como `os.pipe()` o `Queue`, puedo ayudarte con eso también.


# Dudas sobre el TP1

El generador:
```python
def generar_dato():
    '''
    Genera un diccionario por segundo:
    {
       "timestamp": "YYYY-MM-DDTHH:MM:SS",
       "frecuencia": int(60-180),
       "presion": [int(110-180), int(70-110)],
       "oxigeno": int(90-100)
    }
    '''
    # Devuelve un diccionario con los campos frecuencia, presión y oxígeno
    # {"timestamp": "2025-06-11T15:32:09", "frecuencia": 122, "presion": [166, 99], "oxigeno": 100}
    dato = json.dumps({
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "frecuencia": random.randint(60, 180),
        "presion": [random.randint(110, 180), random.randint(70, 110)], # [sistolica, diastolica]
        "oxigeno": random.randint(90, 100)
    })

def generar(pipe_frec,pipe_press,pipe_ox):
    for i in range(60):
        dato = generar_dato()
        pipe_frec.send(dato)
        pipe_press.send(dato)
        pipe_ox.send(dato)
        time.sleep(1)
```
Genera el json de dato cada 1 segundo. Luego se manda el mismo json a los 3 pipes, y cada analizador separa los datos. Esto se podría hacer directamente en el generador. Que directamente envíe los datos que corresponden a cada analizador.