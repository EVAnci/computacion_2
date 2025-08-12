### 1. Fundamentos de Procesos  

#### **¿Qué es un proceso?**  
Un **proceso** es una instancia en ejecución de un programa. Mientras que un **programa** es simplemente un conjunto de instrucciones almacenadas en un archivo, un **proceso** es un programa que se está ejecutando en la memoria del sistema.  

Cada proceso tiene atributos clave que lo identifican y permiten su control, entre ellos:  
- **PID (Process ID):** Identificador único asignado por el sistema operativo.  
- **PPID (Parent Process ID):** Identificador del proceso padre.  
- **Estado:** Puede estar en ejecución, en espera o finalizado.  
- **Espacio de memoria:** Incluye código, datos y pila.  
- **Recursos asignados:** Archivo abiertos, sockets, etc.  

#### **Diferencias entre un programa y un proceso**  
| Característica | Programa | Proceso |
|--------------|-----------|---------|
| Definición | Conjunto de instrucciones almacenadas en un archivo | Instancia en ejecución de un programa |
| Ubicación | Disco duro o SSD | Memoria RAM |
| Estado | Estático | Dinámico (puede cambiar de estado) |
| Identificación | No tiene un identificador único | Tiene un PID único |

#### **Historia y evolución del concepto de procesos**  
Inicialmente, los sistemas operativos ejecutaban un solo programa a la vez (**sistemas monoprogramados**). Con la llegada de **sistemas multiprogramados**, surgió la necesidad de administrar múltiples procesos en paralelo. UNIX fue uno de los primeros sistemas en implementar una gestión avanzada de procesos basada en jerarquías y comunicación entre procesos.

---

Tus respuestas son precisas y bien fundamentadas. ✅  

- En la primera respuesta, captaste la diferencia clave entre un programa (estático) y un proceso (dinámico).  
- En la segunda, mencionaste correctamente el **PCB (Process Control Block)**, que es esencial para la gestión de procesos en el sistema operativo.  
- En la tercera, destacaste la importancia de los **sistemas multiprogramados** y la necesidad de manejar **concurrencia en sistemas modernos**, especialmente en procesadores multinúcleo.  

Ahora, avancemos al siguiente tema.  

---

## 2. **El Modelo de Procesos en UNIX/Linux**  

### **Jerarquía de procesos y herencia**  
En UNIX/Linux, los procesos están organizados en una **jerarquía**. Cada proceso es creado por otro proceso padre, formando un árbol de procesos.  

📌 **Ejemplo de jerarquía en UNIX/Linux:**  
```
PID   PPID  CMD
1     0     systemd
100   1     bash
200   100   python script.py
201   100   nano documento.txt
```
🔹 El proceso **`systemd`** (PID=1) es el primer proceso del sistema y genera otros procesos.  
🔹 **`bash`** (PID=100) es una shell iniciada por systemd.  
🔹 **`python script.py`** (PID=200) y **`nano`** (PID=201) son procesos creados desde la shell.  

Puedes visualizar la jerarquía de procesos con el comando:  
```bash
pstree -p
```
o
```bash
ps -e --forest
```

### **El proceso init/systemd**  
- **init** fue el primer proceso de usuario en UNIX y era responsable de iniciar todos los demás procesos.  
- En distribuciones modernas de Linux, **systemd** ha reemplazado a init.  
- `systemd` inicia servicios, administra demonios y es el proceso raíz con PID **1**.  

Para verificar el proceso padre de un proceso, puedes ejecutar:  
```bash
ps -o pid,ppid,cmd
```

### **Visualización de procesos en Linux**  
Algunas herramientas clave para monitorear procesos:  
- **`ps`** → Muestra procesos en ejecución.  
- **`top`** o **`htop`** → Monitorean procesos en tiempo real.  
- **`kill`** → Finaliza un proceso usando su PID.  
- **`nice`** y **`renice`** → Modifican la prioridad de un proceso.  

Ejemplo para ver los procesos de un usuario específico:  
```bash
ps -u tu_usuario
```

### 🔥 **Sección 3: Manipulación de procesos con Python**  

Ahora vamos a aprender cómo crear y gestionar procesos en Python utilizando llamadas al sistema de UNIX/Linux. Esta es una parte fundamental para comprender cómo se crean y manejan los procesos en sistemas operativos modernos.  

---

## 🧠 **Conceptos clave antes de programar**  

🔹 **`fork()`**  
- Es una llamada al sistema que **crea un nuevo proceso (hijo)** duplicando el proceso actual (padre).  
- Ambos procesos continúan ejecutándose desde la misma línea de código, pero con diferente PID.  
- La única diferencia inicial entre ambos procesos es el valor de retorno de `fork()`:  
  - **El proceso padre** recibe el PID del hijo.  
  - **El proceso hijo** recibe `0`.  

🔹 **`exec()`**  
- Permite **reemplazar** la imagen del proceso actual con un nuevo programa.  
- Se usa cuando queremos que el proceso hijo ejecute un programa completamente distinto del padre.  
- Existen varias variantes como `execl()`, `execv()`, `execle()`, etc., que permiten pasar parámetros y variables de entorno.  

🔹 **`wait()`**  
- Hace que el proceso padre **espere a que el hijo termine** antes de continuar.  
- Esto es útil para evitar que los procesos hijos queden en estado zombi.  

---

## 📌 **Ejemplo 1: Creación de un proceso hijo con `fork()`**  

Veamos un ejemplo básico donde un proceso se duplica y ambos imprimen información sobre sí mismos:  

```python
import os

def main():
    pid = os.fork()  # Se crea un nuevo proceso
    
    if pid > 0:
        print(f"Soy el proceso padre. Mi PID es {os.getpid()} y mi hijo tiene PID {pid}")
    else:
        print(f"Soy el proceso hijo. Mi PID es {os.getpid()} y mi padre tiene PID {os.getppid()}")

if __name__ == "__main__":
    main()
```

### 🔍 **Explicación**  
1. `os.fork()` crea un nuevo proceso duplicando el actual.  
2. Si el valor de `pid` es mayor que 0 → estamos en el **proceso padre**.  
3. Si el valor de `pid` es 0 → estamos en el **proceso hijo**.  
4. Ambos procesos imprimen su información.  

#### 🛠 **Ejecuta el script y observa la salida en la terminal. ¿Notas los dos procesos ejecutándose simultáneamente?**  

---

## 📌 **Ejemplo 2: Uso de `wait()` para sincronización**  

Si queremos asegurarnos de que el padre espere a que su hijo termine antes de continuar, usamos `os.wait()`.  

```python
import os
import time

def main():
    pid = os.fork()

    if pid > 0:
        print(f"Padre esperando que el hijo ({pid}) termine...")
        os.wait()  # El padre espera a que el hijo termine
        print("El hijo ha terminado. El padre continúa.")
    else:
        print(f"Soy el hijo. Mi PID es {os.getpid()}")
        time.sleep(2)  # Simulamos una tarea del hijo
        print("Hijo terminando.")

if __name__ == "__main__":
    main()
```

### 🔍 **Explicación**  
- El padre se bloquea en `os.wait()`, esperando que el hijo termine.  
- El hijo hace `time.sleep(2)`, simulando una tarea, y luego finaliza.  
- Una vez que el hijo termina, el padre sigue su ejecución.  

#### 🛠 **Prueba el código y observa cómo el padre espera a que el hijo termine.**  

---

## 📌 **Ejemplo 3: Uso de `exec()` para ejecutar otro programa**  

A veces queremos que el proceso hijo ejecute otro programa. Podemos hacerlo con `exec()`.  

```python
import os

def main():
    pid = os.fork()

    if pid == 0:  # Proceso hijo
        print(f"Soy el hijo. Voy a ejecutar `ls -l`")
        os.execlp("ls", "ls", "-l")  # Reemplaza el proceso hijo con el comando `ls -l`
    else:
        os.wait()  # El padre espera que el hijo termine
        print("El hijo terminó de ejecutar `ls -l`. El padre continúa.")

if __name__ == "__main__":
    main()
```

### 🔍 **Explicación**  
- El hijo usa `execlp("ls", "ls", "-l")` para reemplazar su código con el comando `ls -l`.  
- **Importante**: `exec()` **no regresa nunca** si la ejecución es exitosa, ya que el código anterior se reemplaza.  
- El padre espera con `wait()` y continúa cuando el hijo termina.  

#### 🛠 **Ejecuta el código y observa cómo el proceso hijo ejecuta `ls -l` en la terminal.**  

---

### ✅ **Pausa para puesta en común**  
Responde estas preguntas antes de continuar:  

1. ¿Cuál es la diferencia fundamental entre `fork()` y `exec()`?  
2. ¿Qué sucede si olvidamos llamar a `os.wait()` en el proceso padre?  
3. ¿Por qué `exec()` no retorna al proceso original después de ejecutarse?  

🚀 **Después de responder, seguimos con procesos zombis y huérfanos.**