# **Módulo `argparse` en Python**

Python proporciona el módulo `argparse`, que simplifica el manejo de argumentos, permitiendo validaciones, argumentos obligatorios, valores predeterminados y mensajes de ayuda automáticos (documentación oficial)

En terminos simples, `argparse` es un módulo de Python que facilita la creación de interfaces de línea de comandos (CLI) de manera robusta y flexible. Es más potente y moderno que `getopt`, y se recomienda su uso para scripts que necesiten manejar argumentos de línea de comandos de manera compleja o extensible.

### Partes principales de `argparse`

1. **ArgumentParser**: Es la clase principal que se utiliza para crear un analizador de argumentos.
2. **Argumentos**: Son las opciones y parámetros que el script acepta. Pueden ser:
   - **Argumentos posicionales**: Se deben proporcionar en un orden específico.
   - **Argumentos opcionales**: Se proporcionan con un nombre (por ejemplo, `-f` o `--file`).
3. **Acciones**: Definen qué hacer con el valor del argumento. Algunas acciones comunes son:
   - `store`: Almacena el valor proporcionado.
   - `store_true` o `store_false`: Almacenan `True` o `False` si la opción está presente.
   - `append`: Almacena múltiples valores en una lista.
4. **Ayuda**: `argparse` genera automáticamente mensajes de ayuda basados en la configuración de los argumentos.

### Uso básico de `argparse`

Aquí se muestra un ejemplo básico de cómo usar `argparse`:

```python
import argparse

def main():
    # Crear un analizador de argumentos
    parser = argparse.ArgumentParser(description="Un script de ejemplo para demostrar argparse.")

    # Añadir argumentos
    parser.add_argument("archivo", help="El archivo de entrada")
    parser.add_argument("-v", "--verbose", action="store_true", help="Activar modo verboso")
    parser.add_argument("-o", "--output", help="Archivo de salida", default="salida.txt")

    # Analizar los argumentos
    args = parser.parse_args()

    # Usar los argumentos
    if args.verbose:
        print(f"Modo verboso activado")
    print(f"Archivo de entrada: {args.archivo}")
    print(f"Archivo de salida: {args.output}")

if __name__ == "__main__":
    main()
```

### Explicación del código

1. **Crear un analizador de argumentos**:
   - `argparse.ArgumentParser(description="...")`: Crea un objeto `ArgumentParser` con una descripción del script.

2. **Añadir argumentos**:
   - `parser.add_argument("archivo", help="...")`: Añade un argumento posicional llamado `archivo`.
   - `parser.add_argument("-v", "--verbose", action="store_true", help="...")`: Añade un argumento opcional `-v` o `--verbose` que almacena `True` si está presente.
   - `parser.add_argument("-o", "--output", help="...", default="salida.txt")`: Añade un argumento opcional `-o` o `--output` con un valor predeterminado.

3. **Analizar los argumentos**:
   - `args = parser.parse_args()`: Analiza los argumentos de la línea de comandos y los almacena en el objeto `args`.

4. **Usar los argumentos**:
   - `args.archivo`, `args.verbose`, `args.output`: Accede a los valores de los argumentos analizados.

### Ejecución

Si ejecutas el script con los siguientes argumentos:

```bash
python script.py entrada.txt -v -o salida_final.txt
```

El output será:

```
Modo verboso activado
Archivo de entrada: entrada.txt
Archivo de salida: salida_final.txt
```

### Argumentos posicionales y opcionales

- **Argumentos posicionales**: Son obligatorios y deben proporcionarse en el orden correcto. En el ejemplo, `archivo` es un argumento posicional.
- **Argumentos opcionales**: No son obligatorios y se pueden proporcionar en cualquier orden. En el ejemplo, `-v` y `-o` son argumentos opcionales.

### Acciones comunes

- **`store`**: Almacena el valor proporcionado (es la acción por defecto).
- **`store_true`/`store_false`**: Almacenan `True` o `False` si la opción está presente.
- **`append`**: Almacena múltiples valores en una lista.

### Ejemplo con acciones

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Ejemplo de acciones en argparse.")
    parser.add_argument("-a", action="store_true", help="Activar opción A")
    parser.add_argument("-b", action="store_false", help="Desactivar opción B")
    parser.add_argument("-c", action="append", help="Añadir valores a la lista")

    args = parser.parse_args()

    print(f"Opción A: {args.a}")
    print(f"Opción B: {args.b}")
    print(f"Opción C: {args.c}")

if __name__ == "__main__":
    main()
```

Ejecutando:

```bash
python script.py -a -b -c valor1 -c valor2
```

El output será:

```
Opción A: True
Opción B: False
Opción C: ['valor1', 'valor2']
```