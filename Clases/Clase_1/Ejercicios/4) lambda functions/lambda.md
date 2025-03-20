## **¿Qué es una función lambda?**
Una **función lambda** en Python es una función anónima (sin nombre) que se define en una sola línea usando la palabra clave `lambda`. Se usa cuando necesitas una función pequeña y rápida sin definirla con `def`.

### **Sintaxis general**
```python
lambda argumentos: expresión
```
Donde:
- `argumentos`: Son los parámetros de la función.
- `expresión`: Es el resultado que devuelve la función.

---

### **Ejemplo 1: Función normal vs función lambda**
Con `def`:
```python
def cuadrado(x):
    return x * x

print(cuadrado(4))  # Salida: 16
```
Con `lambda`:
```python
cuadrado = lambda x: x * x
print(cuadrado(4))  # Salida: 16
```
Ambas funciones hacen lo mismo, pero la versión con `lambda` es más corta.

---

### **Ejemplo 2: Usando `lambda` en `map()` para aplicar una operación a una lista**
```python
numeros = [1, 2, 3, 4]
cuadrados = list(map(lambda x: x**2, numeros))
print(cuadrados)  # Salida: [1, 4, 9, 16]
```
Aquí, `map()` aplica la función `lambda x: x**2` a cada elemento de la lista.

---

### **Ejemplo 3: Usando `lambda` en `sorted()` para ordenar por criterio personalizado**
```python
personas = [("Ana", 25), ("Luis", 30), ("Juan", 20)]
ordenadas = sorted(personas, key=lambda persona: persona[1])
print(ordenadas)  
# Salida: [('Juan', 20), ('Ana', 25), ('Luis', 30)]
```
Aquí, `lambda persona: persona[1]` indica que queremos ordenar la lista por la edad.

---

### **Ejemplo 4: Usando `lambda` en `argparse`**
Podemos reemplazar la función `valid_range` con `lambda`:
```python
parser.add_argument("-x", "--number", type=lambda x: int(x) if 1 <= int(x) <= 100 else argparse.ArgumentTypeError("Número fuera de rango"))
```
Sin embargo, en este caso, **usar una función `def` es mejor**, porque si `lambda` devuelve un error, `argparse` no lo manejará correctamente.

---

### **¿Cuándo usar `lambda` y cuándo `def`?**
✅ Usa `lambda` cuando:
- La función es muy corta y solo tiene una expresión.  
- Se usará inmediatamente como argumento en `map()`, `sorted()`, etc.  

🚨 Usa `def` cuando:
- La función es más compleja o necesita varias líneas.  
- Se reutilizará varias veces en el código.  
- Necesita manejo adecuado de errores y validaciones.  

---
