¡Genial! Ahora vamos a la siguiente sección:  

### **Extensión/Profundización: Manejo de tipos de datos específicos en `argparse`**  

Hasta ahora hemos visto cómo definir argumentos básicos y validaciones con `argparse`, pero también podemos manejar tipos de datos más complejos.  

---  
## **1️⃣ Argumentos tipo `int`, `float` y `bool`**  

Podemos usar los tipos de datos estándar de Python:  
```python
parser.add_argument("--edad", type=int, help="Edad del usuario (número entero)")
parser.add_argument("--altura", type=float, help="Altura en metros (número decimal)")
parser.add_argument("--debug", action="store_true", help="Modo depuración activado")
```
🔹 `type=int`: Convierte el argumento en un número entero.  
🔹 `type=float`: Convierte el argumento en un número decimal.  
🔹 `action="store_true"`: Crea un **flag booleano** (`True` si está presente, `False` si no).  

💡 **Ejemplo de ejecución en terminal:**
```sh
python script.py --edad 25 --altura 1.75 --debug
```
Salida esperada:
```
Edad: 25
Altura: 1.75
Modo depuración: Activado
```
---

## **2️⃣ Argumentos tipo `list` o múltiples valores (`nargs`)**  

🔹 Podemos aceptar **varios valores** en un solo argumento:  
```python
parser.add_argument("--numeros", nargs="+", type=int, help="Lista de números enteros")
```
💡 **Ejemplo de ejecución:**
```sh
python script.py --numeros 1 2 3 4 5
```
Salida esperada:
```
Lista de números: [1, 2, 3, 4, 5]
```
🔹 `nargs="+"` significa **"uno o más valores"**.  

---

## **3️⃣ Argumentos tipo `file` (archivos de entrada y salida)**  

Si un script debe leer o escribir archivos, `argparse` permite validar archivos directamente.  

Ejemplo:  
```python
parser.add_argument("--entrada", type=argparse.FileType("r"), help="Archivo de entrada")
parser.add_argument("--salida", type=argparse.FileType("w"), help="Archivo de salida")
```
💡 **Ejemplo de ejecución:**
```sh
python script.py --entrada datos.txt --salida resultado.txt
```
Esto abrirá `datos.txt` en modo lectura (`r`) y `resultado.txt` en modo escritura (`w`).

---

## **4️⃣ Argumentos tipo `range` (rango de valores válidos)**  

Podemos definir funciones de validación para aceptar rangos específicos.  
Ejemplo:  
```python
def rango_valido(valor):
    valor = int(valor)
    if valor < 1 or valor > 10:
        raise argparse.ArgumentTypeError("Debe estar entre 1 y 10")
    return valor

parser.add_argument("--nivel", type=rango_valido, help="Nivel de dificultad (1-10)")
```
💡 **Ejemplo de ejecución:**
```sh
python script.py --nivel 5  # ✅ Correcto
python script.py --nivel 15 # ❌ Error: "Debe estar entre 1 y 10"
```

---

### **📝 Ejercicio propuesto:**
Crea un script que acepte:  
✅ Un argumento `--archivo` que solo acepte archivos `.txt`.  
✅ Un argumento `--modo` que pueda ser `"rapido"`, `"normal"` o `"lento"`.  
✅ Un argumento `--valores`, que sea una lista de enteros entre 10 y 50.  

💡 **Ejemplo de uso:**  
```sh
python script.py --archivo datos.txt --modo normal --valores 10 20 30
```

📌 **No dudes en preguntarme si necesitas ayuda o validaciones adicionales. ¡Avísame cuando termines! 🚀**