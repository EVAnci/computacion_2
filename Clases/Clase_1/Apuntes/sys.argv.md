# Conceptos fundamentales de `sys.argv`

`sys.argv` es una **lista**. Esta lista contiene los argumentos pasados a un script de python por cli.

Ejemplo:

Veamos básicamente qué hace sys.argv. Creemos un script de python llamado `argv_example_1.py` con el siguiente contenido:

```py
import sys

if __name__ == '__main__':
    print(f'Argumentos: {sys.argv}')
```

El programa anterior, únicamente imprimirá la **lista** de argumentos pasados al script de python. ¿Qué imprimirá?

Si ejecutamos con bash el script tendremos:

```sh
# Entrada
python3 argv_example.py

# Salida
Argumentos: ['argv_example_1.py']
```

Si le pasamos algunos argumentos como `hola mundo` veamos cómo opera:

```sh
# Ejemplo con hola mundo separados por espacio
→ python3 argv_example_1.py hola mundo
Argumentos: ['argv_example_1.py', 'hola', 'mundo']

# Ejemplo cuando ponemos comillas (es equivalente a escapar el caracter espacio con \)
→ python3 argv_example_1.py 'hola mundo' # o también: hola\ mundo
Argumentos: ['argv_example_1.py', 'hola mundo']
```

## Detalles importantes

El primer elemento de la lista `sys.argv` siempre es el nombre del mismo script (o la ruta al script).
Con nuestro conocimiento previo de listas entonces, podríamos acceder a cada uno de los elementos del array:

```py
sys.argv[0] # Nombre o ruta del script.
sys.argv[1] # Primer argumento recibido.
sys.argv[2] # Segundo argumento recibido.
```

Otra cosa que podríamos hacer es ver todos los argumentos recibidos sin incluir el propio nombre del script:

```py
sys.argv[1:] 
```

Con el método de acceso anterior, lo que hacemos es recortar la lista, accediendo desde el índice 1 en adelante.

# Vease también

[Mastering `sys.argv`](https://coderivers.org/blog/python-sys.argv/)