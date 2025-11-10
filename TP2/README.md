# Una breve explicación 

El trabajo consiste de dos servidores principales ubicados en la raíz del proyecto:
- `server_scrapping.py`
- `server_processing.py`

Estos servidores son los encargados de realizar el trabajo pedido en la consigna. A continuación explicaré algunos detalles a tener en cuenta para la ejecución.

## Ejecución de servidores

Los servidores A y B tienen su interfaz de línea de comandos realizada con argparse. Para ejecutarlos se pueden seguir esas instrucciones. El servidor A (como se pedía en la consigna) acepta el protocolo IPv4 e IPv6 ya que el módulo web de aiohttp ya soporta por defecto ambos protocolos. El Servidor B solo acepta IPv4. De esa forma podría estar en un host distinto al que contiene al Servidor A y funcionar exactamente igual.

Un ejemplo de ejecución requiere al menos dos terminales (o lanzar dos procesos distintos en la misma terminal). Ejemplo:
```sh
# Para el Servidor A
python server_scraping.py -i ::1 -p 8080
```
Esto lanza el Servidor A en localhost (IPv6) en el puerto 8080.
```sh
# Para el servidor B
python server_processing.py -i 127.0.0.2 -p 8000
```
Esto lanza el Servidor B en localhost (IPv4) en el puerto 8000. Es importante que si no se usan estos valores de IP y puerto (que son valores por defecto) se especifiquen en el servidor A usando las opciones correspondientes (`b_ip` y `b_port`).

Es necesario tener un entorno virtual y haber instalado los paquetes en requirements.txt para que funcione.

### Ejecución de algunas pruebas

Pues está claro que los datos que se reciben en formato json son texto plano... Por lo tanto, las imágenes estan codificadas en base 64. Esto es súper útil si queremos enviar la imágen usando un protocolo de texto (como http), pero si queremos verla está dificil. 

El cliente nos permite probar la funcionalidad de una forma super sencilla. En vez de hacer POST requests con `curl` podemos usar 
```sh
python client.py -t
```
Esto permite lanzar un conjunto de 10 urls de prueba para que no debas escribirlas a mano. Si quieres probar una o más urls específicas puedes usar
```sh
python client.py https://url1.net https://url2.net ... 
```
Para que todo esto funcione sin más parámetros adicionales debemos usar los comandos de ejecución dados en la parte superior. Si hemos lanzado el servidor A usando otra dirección IP y otro puerto debemos especificarlo usando los argumentos especificados en el mensaje de ayuda de la interfaz cli del cliente.

El cliente por si mismo guarda los json del análisis en un directorio `pages/url/` correspondiente a cada request, donde podemos analizar los datos más tranquilos y ver las imágenes y miniaturas en el directorio `pages/url/media/`.

También he realizado dos scripts en bash. Uno para probar algunas url usando varios procesos llamado `sAtester.sh` (o server A tester) y otro llamado `screen_viewer.sh` para visualizar las imágenes de una forma más manual. Estos scripts tienen unos detalles para su uso, ya que no prioricé la lógica del script sinó más bien la simplicidad y que sea útil para hacer pruebas planas.

Estos scripts están pensados para funcionar cuando se lanza el Servidor A en `localhost:8080`. Para probarlos y ver las imágenes hacemos lo siguiente:
```sh
./sAtester.sh
```
El script hará todo su trabajo y guardará los json recibidos en `pages/`. Luego podemos ejecutar
```sh
./screen_viewer.sh pages/nombre_de_la_pagina.com # Sin .json
```
que decodificará las solo las capturas de panatalla y las guardará en archivos distintos.

> [!NOTE] 
> Estos scripts pueden tener bashismos (no son totalmente fiel al estandard POSIX) así que si quieres probar los scripts recomiendo probarlos usando bash.
> Las cabeceras del script ya sugieren a la sesión de ejecución que use bash, pero si tienes enlaces simbólicos no puedo garantizar que funcionen.

## Datos sobre el diseño

### Servidor A

El Servidor A se pedía asíncrono. Entonces utiliza el módulo `asyncio` de python. Esto nos permite manejar las tareas IO/Bound aprobechando mejor el tiempo, ya que estamos usando greentheads para manejar cada solicitud. En este caso la "magia" sucede en la función `scraper/fetch_url` que es asíncrona y por tanto no bloquea el hilo principal de ejecución (que es manejado por el scheduler de asyncio).

### Servidor B

El servidor B se encarga de tareas CPU/Bound, entonces los greentheads no nos sirven. En este caso he preferido utilizar un pool de procesos `ProcessPoolExecutor` ya que es bueno justamente para tareas CPU/Bound (porque no se ve afectado por el GIL de python). Este servidor lanza procesos a medida que se reciben requests del Servidor A. Cada proceso ejecuta las siguientes tareas de forma secuencial:
- Captura del sitio web
- Análisis de rendimiento
- Generación de miniatura de las imágenes

Estas tareas se realizan llamando a la función `run_full_analysis`. ¿Por qué he decidido ejecutar estas tareas CPU/Bound secuencialmente para cada request? La respuesta es sencilla: **selenium**. 

El módulo `selenium` de python permite lanzar un navegador (y usando la opción headless es más liviano). El problema está en que el driver (o navegador del módulo selenium) es lo suficientemente complejo y grande como para que demore más el propio driver en inicializarse, y cada uno de los drivers hacer la misma request get a la url, que el analisis completo de las requests. Entonces la solución más optima es usar un solo driver para hacer todas las tareas. Y para evitar bloqueos al recibir requests (o urls) cada request (url) usa su propio driver en su propio proceso.

¿Y por qué no compartí el driver entre multiples procesos? Porque no es del todo factible. Para compartir el driver completo deberíamos tener un IPC entre los 3 procesos (que hacen las 3 tareas del run_full_analysis) capaz de compartir el bloque de memoria usado por el driver. Además deben estar los 3 sincronizados y evitar problemas típicos de concurrencia (exclusión mútua, condiciones de carrera). Esto hacía más complicado pensar en cómo solucionar dicho problema de IPC que el propio trabajo práctico y la ganancia de rendimiento no sería completamente notoria.

### El protocolo de comunicación entre servidores

Para el protocolo busqué la simplicidad ante todo lo posible. Utilicé un protocolo por tamaño. Entonces se envían y reciben "chunks" de datos del mismo tamaño.
