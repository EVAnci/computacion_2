# Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

## Diseño del proyecto

El diseño general se realizó siguiendo una estructura de archivos y directorios sugerida por ChatGPT:
```bash
src
├── __init__.py
├── analizador.py
├── blockchain.py
├── generador.py
├── utils.py
└── verificador.py
tests -directorio
args.py
blockchain.json
main.py
reporte.txt
verificar_cadena.py
```
Esta estructura me resultó adecuada ya que es cómoda y modular para separar las responsabilidades de cada proceso.

## Ejecución

Para ejecutar el programa se ha creado una interfaz cli usando argparse. Puede usar el comando:

```sh
python3 main.py
```

Y esto tomará los valores por defecto (60 bloques). Para modificar la cantidad de bloques puede usar el parametro `-h` para ver las opciones disponibles.
```sh
python3 main.py -h
```

### El modelo de procesos e IPC

Respetando la consigna dada, el modelo general de procesos que se obtiene al ejectar el código es el siguiente:

- El proceso principal que se encarga de lanzar y esperar a todos los demás procesos
- El proceso generador que se encarga de generar 1 dato por segundo con el formato especificado
- Los procesos analizadores (3 procesos) que se encargan de separar y analizar un dato particular de los datos generados por el proceso generador
- El proceso verificador que se encarga de juntar los datos procesados por los analizadores y formar una cadena de bloques

Para la creación de procesos he decidido utilizar utilizar la librería `multiprocessing` en vez de `os` ya que facilita la creación de procesos y evita los problemas típicos que pueden suceder con `fork` (como no esperar correctamente que un proceso finalice o no detener correctamente los procesos hijos cuando terminan de ejecutar la función objetivo).

#### IPC entre procesos

La comunicación y la elección de cada método de comunicación son las siguientes:

- La comunicación entre el generador y los analizadores se utiliza un pipe por cada analizador. La principal razón de esta elección es porque la librería `multiprocessing` tiene `Pipe` para gestionar los file-descriptors, abrir, cerrar y manejar las secciones críticas cuando se escribe y cuando se lee el pipe. La ventaja de pipes sobre fifos (o named pipes) es que en la consigna se solicita un pipe o fifo por proceso, y los pipes anónimos son más adecuados para esta tarea, ya que se crean en el contexto de los procesos que se comunican y no permiten que otros procesos externos puedan adquirir el pipe. Además el pipe anónimo es más secillo de implementar.
- La consigna sugiere utilizar Queues para comunicar los procesos analizadores con el proceso verificador. El uso de Queues en este apartado se justifica por dos motivos principales: existe una abstracción a alto nivel en la librería `multiprocessing` y múltiples procesos pueden escribir en la cola (uno por vez) y otro proceso puede consumir los datos que están en la misma. 
