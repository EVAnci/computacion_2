# ¿Qué es getopt?

Según la [documentación oficial de python](https://docs.python.org/3/library/getopt.html) es un módulo que ayuda a gestionar los argumentos recibidos con `sys.argv`.

Entonces básicamente el módulo `getopt` en Python que se utiliza para analizar opciones de línea de comandos y argumentos. Es similar a la función `getopt()` en C y es útil para manejar argumentos pasados a un script desde la terminal. Si no has usado C no hay problema, no es necesario para aprender a usar este módulo en Python.

# ¿Cómo se usa?

Bueno, `getopt` nos provee de **dos funciones** y **una excepción**. 

## Función `getopt.getopt()`

La función `getopt.getopt(args, shortopts, longopts=[])` recibe 3 argumentos. 

El primer argumento suele ser la lista de argumentos `argv[:1]` recibidos en la cli. El segundo argumento es de tipo **string** y permite indicar las opciones abreviadas o en formato acortado. Por último el tercer argumento recibe una lista con todos los argumentos en formato largo.

1. **args**: La lista de argumentos que se va a analizar (normalmente `sys.argv[1:]`).
2. **shortopts**: Una cadena que especifica las opciones cortas (de un solo carácter) que el script acepta.
3. **longopts**: Una lista de cadenas que especifica las opciones largas (de múltiples caracteres) que el script acepta.

Esta función retorna 2 valores:

1. **opts**: Una lista de tuplas `(opción, valor)` que representan las opciones y sus valores.
2. **args**: Una lista de los argumentos restantes que no son opciones.

### Sintaxis

```python
# Importamos las librerias necesarias
import getopt
import sys

# Tomamos los argumentos con sys.argv
arguments = sys.argv[:1]

# Como getopt.getopt retorna dos valores, podemos almacenar cada uno en variables distintas:
opts, args = getopt.getopt(arguments, shortopts, longopts=[])
```

### Ejemplo de uso

Supongamos que tienes un script que acepta las siguientes opciones:

- `-h` o `--help`: Muestra la ayuda.
- `-v` o `--verbose`: Activa el modo verboso.
- `-m <mensaje>` o `--message=<mensaje>`: Especifica un mensaje de salida.

Entonces para indicarle estos argumentos a `getopt.getopt()` podemos realizar lo siguiente:

```py
import sys, getopt

arguments = sys.argv[:1]
opts, args = getopt.getopt(arguments, "hvm:", ["help", "verbose", "message="])

# Luego definimos la lógica de nuestro script
# En este caso solo vamos a imprimir todas las opciones contempladas y los argumentos adicionales
print(f'Opciones: {opts}')
print(f'Argumentos: {args}')
```

En este punto seguro te preguntaras: ¿Qué hacen esos dos puntos o ese signo "igual" en mis opciones de mensaje?

La respuesta es bastante sencilla. En argumentos cortos indicaremos con `m:` que la opción `m` espera que tenga un valor. Esto quiere decir que si usamos sólo `-m` no funcionará. Si o si debemos escribir `-m algo`, donde `algo` será una cadena. Para el formato largo, el "igual" (`=`) cumple la misma función.

Entonces, siempre y cuando pasemos al script los siguientes argumentos:

- `-h` o `--help`
- `-v` o `--verbose`
- `-m 'un mensaje cualquiera'` o `--message 'un mensaje cualquiera'`

se van a almacenar en la variable `opts` (de la palabra options en inglés). 
Si pasamos cualquier otro argumento como `algo`, `hola` o cualquier otra cosa, se almacenará en la variable `args`.

## Función `getopt.gnu_getopt()`

La función `gnu_getopt()` en Python es una variante de `getopt()` que sigue las convenciones de estilo GNU para el análisis de argumentos de línea de comandos. La principal diferencia entre `getopt()` y `gnu_getopt()` radica en cómo manejan los argumentos que no son opciones (es decir, argumentos que no comienzan con `-` o `--`).

### Diferencias clave entre `getopt()` y `gnu_getopt()`

1. **Comportamiento por defecto**:
   - **`getopt()`**: Detiene el procesamiento de opciones tan pronto como encuentra un argumento que no es una opción (es decir, un argumento que no comienza con `-` o `--`). Esto significa que todos los argumentos que no son opciones deben venir después de las opciones.
   - **`gnu_getopt()`**: Permite que los argumentos de opciones y los que no son opciones se mezclen. Esto es conocido como "modo de escaneo estilo GNU".

2. **Modo POSIX**:
   - Si el primer carácter de la cadena de opciones es `+`, o si la variable de entorno `POSIXLY_CORRECT` está configurada, entonces `gnu_getopt()` se comportará como `getopt()`, deteniendo el procesamiento de opciones al encontrar un argumento que no es una opción.

### Ejemplo para ilustrar la diferencia

Supongamos que tienes un script que acepta las siguientes opciones:

- `-a`: Opción sin argumento.
- `-b`: Opción con argumento.

#### Usando `getopt()`

```python
import getopt
import sys

arguments = sys.argv[1:]
opts, args = getopt.getopt(arguments, "ab:")

# iteramos sobre la lista de tuplas opts
# como cada elemento es una tupla de 2 elementos podemos acceder a ambos en el for.
for opt, arg in opts:
    if opt == '-a':
        print('Opción -a')
    elif opt == '-b':
        print(f'Opción -b con argumento: {arg}')

print(f'Argumentos restantes: {args}')
```

Si ejecutas este script con:

```bash
python script.py -a -b valor arg1 arg2
```

El output será:

```
Opción -a
Opción -b con argumento: valor
Argumentos restantes: ['arg1', 'arg2']
```

Pero si ejecutas:

```bash
python script.py -a arg1 -b valor arg2
```

El output será:

```
Opción -a
Argumentos restantes: ['arg1', '-b', 'valor', 'arg2']
```

Aquí, `getopt()` detuvo el procesamiento de opciones al encontrar `arg1`, y no procesó `-b valor`.

#### Usando `gnu_getopt()`

```python
import getopt
import sys

arguments = sys.argv[1:]
opts, args = getopt.gnu_getopt(arguments, "ab:")

for opt, arg in opts:
    if opt == '-a':
        print('Opción -a')
    elif opt == '-b':
        print(f'Opción -b con argumento: {arg}')

print(f'Argumentos restantes: {args}')
```

Si ejecutas este script con:

```bash
python script.py -a arg1 -b valor arg2
```

El output será:

```
Opción -a
Opción -b con argumento: valor
Argumentos restantes: ['arg1', 'arg2']
```

Aquí, `gnu_getopt()` permitió que `arg1` se mezclara con las opciones y aún así procesó `-b valor`.

### Modo POSIX

Si cambias la cadena de opciones a `"+ab:"` o configuras la variable de entorno `POSIXLY_CORRECT`, `gnu_getopt()` se comportará como `getopt()`.

## Excepción `getopt.GetoptError`

`getopt.GetoptError` es una excepción que se lanza cuando ocurre un error durante el análisis de las opciones de línea de comandos utilizando las funciones `getopt.getopt()` o `getopt.gnu_getopt()` en Python. Esta excepción es útil para manejar situaciones en las que el usuario proporciona opciones no válidas o argumentos incorrectos.

### Causas comunes de `getopt.GetoptError`

1. **Opción no reconocida**: El usuario proporciona una opción que no está definida en la cadena de opciones cortas (`shortopts`) o en la lista de opciones largas (`longopts`).
2. **Falta de argumento**: El usuario proporciona una opción que requiere un argumento, pero no lo incluye.
3. **Argumento no esperado**: El usuario proporciona un argumento para una opción que no lo requiere.

### Estructura de `getopt.GetoptError`

La excepción `getopt.GetoptError` tiene dos atributos principales:

- **msg**: Un mensaje de error que describe el problema.
- **opt**: La opción que causó el error (si es aplicable).

### Ejemplo de manejo de `getopt.GetoptError`

Es más fácil entenderlo viendo un ejemplo de cómo manejar esta excepción en un script:

```python
import getopt
import sys

try:
    # Definir los argumentos y las opciones cortas y largas
    arguments = sys.argv[1:]
    opts, args = getopt.getopt(argv, "ho:v", ["help", "output=", "verbose"])
except getopt.GetoptError as err:
    # Manejar la excepción
    print(f"Error: {err.msg}")
    print(f"Opción problemática: {err.opt}")
    print('Uso: script.py -h -o <archivo> -v')
    sys.exit(2)

output_file = None
verbose = False

# Procesar las opciones
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print('Uso: script.py -h -o <archivo> -v')
        sys.exit()
    elif opt in ('-o', '--output'):
        output_file = arg
    elif opt in ('-v', '--verbose'):
        verbose = True

# Mostrar los resultados
if verbose:
    print('Modo verboso activado')
if output_file:
    print(f'Archivo de salida: {output_file}')
print(f'Argumentos restantes: {args}')
```

### Ejecución y manejo de errores

#### Caso 1: Opción no reconocida

Si ejecutas el script con una opción no reconocida:

```bash
python script.py -x
```

El output será:

```
Error: option -x not recognized
Opción problemática: -x
Uso: script.py -h -o <archivo> -v
```

#### Caso 2: Falta de argumento

Si ejecutas el script con una opción que requiere un argumento, pero no lo proporcionas:

```bash
python script.py -o
```

El output será:

```
Error: option -o requires argument
Opción problemática: -o
Uso: script.py -h -o <archivo> -v
```

#### Caso 3: Argumento no esperado

Si ejecutas el script con un argumento para una opción que no lo requiere:

```bash
python script.py -h argumento_extra
```

El output será:

```
Error: option -h does not take an argument
Opción problemática: -h
Uso: script.py -h -o <archivo> -v
```

# Importante

Todo lo que hemos visto es para comprender el uso de la forma más sencilla posible. Ahora, cada vez que realicemos un script utilizando este módulo, debemos hacerlo de la forma recomendada en Python, envolviendo todo el código en una función y utilizando la estructura `if __name__ == '__main__'`. Entonces el resultado final quedaría algo así:

```python
import getopt
import sys

def main(argv):
    try:
        # Definir las opciones cortas y largas
        opts, args = getopt.getopt(argv, "ho:v", ["help", "output=", "verbose"])
    except getopt.GetoptError as err:
        # Manejar la excepción
        print(f"Error: {err.msg}")
        print(f"Opción problemática: {err.opt}")
        print('Uso: script.py -h -o <archivo> -v')
        sys.exit(2)

    output_file = None
    verbose = False

    # Procesar las opciones
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('Uso: script.py -h -o <archivo> -v')
            sys.exit()
        elif opt in ('-o', '--output'):
            output_file = arg
        elif opt in ('-v', '--verbose'):
            verbose = True

    # Mostrar los resultados
    if verbose:
        print('Modo verboso activado')
    if output_file:
        print(f'Archivo de salida: {output_file}')
    print(f'Argumentos restantes: {args}')

if __name__ == "__main__":
    main(sys.argv[1:])
```

### Explicación del código

1. **Definición de opciones**:
   - `"ho:v"`: Las opciones cortas. `h` y `v` no requieren argumentos adicionales, mientras que `o` requiere un argumento (por eso tiene `:`).
   - `["help", "output=", "verbose"]`: Las opciones largas. `output=` indica que `--output` requiere un argumento.

2. **Manejo de errores**:
   - Si el usuario proporciona una opción no válida, `getopt.GetoptError` se lanza y se maneja imprimiendo las características del error.

3. **Procesamiento de opciones**:
   - Se itera sobre las opciones y se actúa en consecuencia. Por ejemplo, si se encuentra `-v` o `--verbose`, se activa el modo verboso.

4. **Argumentos restantes**:
   - Los argumentos que no son opciones se almacenan en `args`.

### Ejecución

Si ejecutas el script con los siguientes argumentos:

```bash
python script.py -v -o salida.txt archivo1 archivo2
```

El output será:

```
Modo verboso activado
Archivo de salida: salida.txt
Argumentos restantes: ['archivo1', 'archivo2']
```